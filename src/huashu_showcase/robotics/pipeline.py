"""Pipelines for question-level robotics optimization."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from huashu_showcase.config import ArmConfig, DEFAULT_ARM_CONFIG
from huashu_showcase.robotics.ga import GAConfig, GAResult, GeneticOptimizer
from huashu_showcase.robotics.model import (
    assemble_joint_angles_rad,
    distance_error_mm,
    endpoint_mm,
    gravitational_work_joule,
    joint_energy_cost,
)


@dataclass(frozen=True)
class RoboticsOptimizationResult:
    title: str
    objective_name: str
    ga_result: GAResult
    best_norm_params: np.ndarray
    best_joint_angles_rad: np.ndarray
    endpoint_mm: np.ndarray
    distance_mm: float
    gravity_work_joule: float
    energy_per_joint_joule: np.ndarray
    total_motion_energy_joule: float


def default_ga_config(seed: int = 42) -> GAConfig:
    return GAConfig(
        population_size=220,
        generations=140,
        crossover_rate=0.92,
        mutation_rate=0.2,
        mutation_scale=0.06,
        elite_size=3,
        tournament_size=4,
        seed=seed,
    )


def _build_result(
    title: str,
    objective_name: str,
    ga_result: GAResult,
    config: ArmConfig,
) -> RoboticsOptimizationResult:
    best_norm = ga_result.best_individual
    best_joint = assemble_joint_angles_rad(best_norm, config)
    endpoint = endpoint_mm(best_norm, config)
    distance = distance_error_mm(best_norm, config)
    gravity = gravitational_work_joule(best_norm, config)
    joint_energy = joint_energy_cost(best_joint, config)

    return RoboticsOptimizationResult(
        title=title,
        objective_name=objective_name,
        ga_result=ga_result,
        best_norm_params=best_norm,
        best_joint_angles_rad=best_joint,
        endpoint_mm=endpoint,
        distance_mm=distance,
        gravity_work_joule=gravity,
        energy_per_joint_joule=joint_energy,
        total_motion_energy_joule=float(np.sum(joint_energy)),
    )


def run_question1(
    config: ArmConfig = DEFAULT_ARM_CONFIG,
    ga_config: GAConfig | None = None,
) -> RoboticsOptimizationResult:
    ga_config = ga_config or default_ga_config(seed=42)
    bounds = np.array([[0.0, 1.0], [0.0, 1.0], [0.0, 1.0]], dtype=float)

    optimizer = GeneticOptimizer(
        objective=lambda x: distance_error_mm(x, config),
        bounds=bounds,
        config=ga_config,
    )
    result = optimizer.run()

    return _build_result(
        title="第一问: 末端定位优化",
        objective_name="min distance_error_mm",
        ga_result=result,
        config=config,
    )


def run_question2(
    weight_distance: float = 0.7086,
    weight_gravity: float = 0.2228,
    config: ArmConfig = DEFAULT_ARM_CONFIG,
    ga_config: GAConfig | None = None,
) -> RoboticsOptimizationResult:
    ga_config = ga_config or default_ga_config(seed=84)
    bounds = np.array([[0.0, 1.0], [0.0, 1.0], [0.0, 1.0]], dtype=float)

    def objective(norm_params: np.ndarray) -> float:
        return (
            weight_distance * distance_error_mm(norm_params, config)
            + weight_gravity * gravitational_work_joule(norm_params, config)
        )

    optimizer = GeneticOptimizer(objective=objective, bounds=bounds, config=ga_config)
    result = optimizer.run()

    return _build_result(
        title="第二问: 多目标加权优化",
        objective_name=f"min {weight_distance:.4f}*distance + {weight_gravity:.4f}*gravity",
        ga_result=result,
        config=config,
    )
