"""Robotics optimization modules."""

from .ga import GAConfig, GAResult, GeneticOptimizer
from .model import (
    assemble_joint_angles_rad,
    denormalize_angles_rad,
    distance_error_mm,
    endpoint_mm,
    gravitational_work_joule,
    joint_energy_cost,
    solve_wrist_angles_rad,
)
from .pipeline import RoboticsOptimizationResult, run_question1, run_question2

__all__ = [
    "GAConfig",
    "GAResult",
    "GeneticOptimizer",
    "RoboticsOptimizationResult",
    "assemble_joint_angles_rad",
    "denormalize_angles_rad",
    "distance_error_mm",
    "endpoint_mm",
    "gravitational_work_joule",
    "joint_energy_cost",
    "solve_wrist_angles_rad",
    "run_question1",
    "run_question2",
]
