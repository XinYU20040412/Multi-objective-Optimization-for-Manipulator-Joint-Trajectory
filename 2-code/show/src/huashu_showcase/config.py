"""Global configuration and constants."""

from __future__ import annotations

from dataclasses import dataclass
from math import pi


@dataclass(frozen=True)
class ArmConfig:
    """Robot arm geometry and dynamic constants."""

    target_mm: tuple[float, float, float] = (1500.0, 1200.0, 200.0)
    link1_mm: float = 300.0
    link2_mm: float = 1200.0
    link3_mm: float = 1500.0
    base_height_mm: float = 600.0

    # The original scripts use these values for inertia energy estimation.
    theta0_rad: tuple[float, ...] = (0.0, -pi / 2.0, 0.0, pi, -pi / 2.0, 0.0)
    omega_mean_deg_s: tuple[float, ...] = (2.0, 1.5, 1.0, 2.5, 3.0, 2.0)
    inertia: tuple[float, ...] = (0.5, 0.3, 0.4, 0.6, 0.2, 0.4)

    # Potential-energy model constants.
    arm_mass_kg: float = 5.0
    gravity: float = 9.8


DEFAULT_ARM_CONFIG = ArmConfig()
