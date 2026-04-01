"""Kinematics and objective functions for question 1 and 2."""

from __future__ import annotations

from math import atan2, cos, pi, sin, sqrt

import numpy as np

from huashu_showcase.config import ArmConfig, DEFAULT_ARM_CONFIG


ANGLE_SCALE_DEG = np.array([320.0, 165.0, 280.0], dtype=float)
ANGLE_OFFSET_DEG = np.array([-160.0, -60.0, -200.0], dtype=float)


def clamp_normalized(norm_params: np.ndarray) -> np.ndarray:
    return np.clip(np.asarray(norm_params, dtype=float), 0.0, 1.0)


def denormalize_angles_rad(norm_params: np.ndarray) -> np.ndarray:
    norm_params = clamp_normalized(norm_params)
    deg = norm_params * ANGLE_SCALE_DEG + ANGLE_OFFSET_DEG
    return np.deg2rad(deg)


def _r2_1(a1: float, config: ArmConfig) -> np.ndarray:
    return np.array(
        [
            [cos(a1), 0.0, sin(a1), config.link1_mm * cos(a1)],
            [sin(a1), 0.0, -cos(a1), config.link1_mm * sin(a1)],
            [0.0, 1.0, 0.0, config.base_height_mm],
            [0.0, 0.0, 0.0, 1.0],
        ],
        dtype=float,
    )


def _r3_2(a2: float, config: ArmConfig) -> np.ndarray:
    return np.array(
        [
            [cos(a2), -sin(a2), 0.0, config.link2_mm * cos(a2 + pi / 2.0)],
            [sin(a2), cos(a2), 0.0, config.link2_mm * sin(a2 + pi / 2.0)],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0],
        ],
        dtype=float,
    )


def _r4_3(a3: float, config: ArmConfig) -> np.ndarray:
    return np.array(
        [
            [0.0, cos(a3), cos(pi / 2.0 + a3), config.link3_mm * cos(pi / 2.0 + a3)],
            [0.0, sin(a3), sin(pi / 2.0 + a3), config.link3_mm * sin(pi / 2.0 + a3)],
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 1.0],
        ],
        dtype=float,
    )


def endpoint_mm(norm_params: np.ndarray, config: ArmConfig = DEFAULT_ARM_CONFIG) -> np.ndarray:
    a1, a2, a3 = denormalize_angles_rad(norm_params)
    x4 = np.array(
        [
            config.link3_mm * cos(pi / 2.0 + a3),
            config.link3_mm * sin(pi / 2.0 + a3),
            0.0,
            1.0,
        ],
        dtype=float,
    )
    transform = _r2_1(a1, config) @ _r3_2(a2, config)
    point = transform @ x4
    return point[:3]


def target_in_frame4(norm_params: np.ndarray, config: ArmConfig = DEFAULT_ARM_CONFIG) -> np.ndarray:
    a1, a2, a3 = denormalize_angles_rad(norm_params)
    target_h = np.array([*config.target_mm, 1.0], dtype=float)
    transform = _r2_1(a1, config) @ _r3_2(a2, config) @ _r4_3(a3, config)
    point = np.linalg.solve(transform, target_h)
    return point[:3]


def solve_wrist_angles_rad(norm_params: np.ndarray, config: ArmConfig = DEFAULT_ARM_CONFIG) -> np.ndarray:
    x0, y0, z0 = target_in_frame4(norm_params, config)
    xy_len = sqrt(max(x0 * x0 + y0 * y0, 1e-12))

    # atan2 is numerically safer than acos in the original script.
    a = atan2(y0, x0)
    b = atan2(z0, xy_len)

    a4 = a - 2.0 * pi
    a5 = 0.0
    a6 = pi / 2.0 - b
    return np.array([a4, a5, a6], dtype=float)


def assemble_joint_angles_rad(norm_params: np.ndarray, config: ArmConfig = DEFAULT_ARM_CONFIG) -> np.ndarray:
    first_three = denormalize_angles_rad(norm_params)
    wrist = solve_wrist_angles_rad(norm_params, config)
    return np.concatenate([first_three, wrist])


def distance_error_mm(norm_params: np.ndarray, config: ArmConfig = DEFAULT_ARM_CONFIG) -> float:
    endpoint = endpoint_mm(norm_params, config)
    target = np.asarray(config.target_mm, dtype=float)
    return float(np.linalg.norm(endpoint - target))


def gravitational_work_joule(norm_params: np.ndarray, config: ArmConfig = DEFAULT_ARM_CONFIG) -> float:
    a1, a2, _ = denormalize_angles_rad(norm_params)

    p3_2 = np.array(
        [
            config.link2_mm * cos(pi / 2.0 + a2),
            config.link2_mm * sin(pi / 2.0 + a2),
            0.0,
            1.0,
        ],
        dtype=float,
    )
    p3 = _r2_1(a1, config) @ p3_2

    z3 = p3[2] * 1e-3
    z4 = endpoint_mm(norm_params, config)[2] * 1e-3
    z2 = config.base_height_mm * 1e-3

    total_length_m = (config.base_height_mm + config.link1_mm + config.link2_mm + config.link3_mm) * 1e-3
    m = config.arm_mass_kg
    g = config.gravity

    ef = (
        (config.link1_mm * 1e-3 / total_length_m) * z2 * m * g
        + (config.link2_mm * 1e-3 / total_length_m) * m * g * (z2 + z3) / 2.0
        + (config.link3_mm * 1e-3 / total_length_m) * m * g * (z4 + z3) / 2.0
    )
    e0 = m * g * total_length_m / 2.0
    return float(e0 - ef)


def joint_energy_cost(theta_rad: np.ndarray, config: ArmConfig = DEFAULT_ARM_CONFIG) -> np.ndarray:
    theta_rad = np.asarray(theta_rad, dtype=float)
    if theta_rad.shape != (6,):
        raise ValueError("theta_rad must have shape (6,)")

    energies = np.zeros(6, dtype=float)

    for idx, delta in enumerate(theta_rad):
        # Follow the legacy assumption: joint 5 does not consume motion energy.
        if idx == 4 or abs(delta) < 1e-12:
            continue

        omega_deg_s = config.omega_mean_deg_s[idx]
        inertia = config.inertia[idx]
        duration = abs(delta) * 180.0 / (pi * omega_deg_s)
        if duration <= 1e-12:
            continue

        # Closed-form value of the original integral formulation.
        energies[idx] = 0.6 * inertia * (delta**2) / (duration**2)

    return energies


def total_motion_energy_joule(norm_params: np.ndarray, config: ArmConfig = DEFAULT_ARM_CONFIG) -> float:
    theta = assemble_joint_angles_rad(norm_params, config)
    return float(np.sum(joint_energy_cost(theta, config)))
