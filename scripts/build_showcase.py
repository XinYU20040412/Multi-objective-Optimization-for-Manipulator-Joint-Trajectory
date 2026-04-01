"""Build all showcase artifacts (figures + GIFs + summary markdown)."""

# pyright: reportMissingImports=false

from __future__ import annotations

from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from huashu_showcase.ahp import compute_ahp
from huashu_showcase.graph import solve_hamiltonian
from huashu_showcase.path_planning import ACOConfig, AntColonyPlanner, default_demo_grid
from huashu_showcase.robotics import run_question1, run_question2
from huashu_showcase.visualization import (
    plot_ahp_weights,
    plot_ga_history,
    plot_hamiltonian_cycle,
    plot_path_grid,
    save_aco_path_gif,
    save_ga_evolution_gif,
    save_showcase_cover_gif,
)


def ensure_dirs(root: Path) -> tuple[Path, Path]:
    fig_dir = root / "assets" / "figures"
    gif_dir = root / "assets" / "gifs"
    fig_dir.mkdir(parents=True, exist_ok=True)
    gif_dir.mkdir(parents=True, exist_ok=True)
    return fig_dir, gif_dir


def run_robotics(fig_dir: Path, gif_dir: Path) -> tuple[dict[str, float], np.ndarray, np.ndarray, np.ndarray]:
    q1 = run_question1()
    q2 = run_question2()

    plot_ga_history(
        q1.ga_result.history_best,
        q1.ga_result.history_mean,
        title="Question 1 GA Convergence",
        output_path=str(fig_dir / "q1_ga_history.png"),
    )

    plot_ga_history(
        q2.ga_result.history_best,
        q2.ga_result.history_mean,
        title="Question 2 GA Convergence",
        output_path=str(fig_dir / "q2_ga_history.png"),
    )

    save_ga_evolution_gif(
        q2.ga_result.best_trace,
        output_path=str(gif_dir / "ga_evolution.gif"),
    )

    metrics = {
        "q1_distance_mm": q1.distance_mm,
        "q1_energy_joule": q1.total_motion_energy_joule,
        "q2_distance_mm": q2.distance_mm,
        "q2_gravity_joule": q2.gravity_work_joule,
        "q2_energy_joule": q2.total_motion_energy_joule,
    }

    return metrics, q2.ga_result.history_best, q2.ga_result.history_mean, q2.ga_result.best_trace


def run_ahp(fig_dir: Path) -> dict[str, float]:
    matrix = np.array(
        [
            [1.0, 5.0, 7.0],
            [1.0 / 5.0, 1.0, 5.0],
            [1.0 / 7.0, 1.0 / 5.0, 1.0],
        ],
        dtype=float,
    )

    result = compute_ahp(matrix)
    plot_ahp_weights(result, output_path=str(fig_dir / "ahp_weights.png"))

    return {
        "ahp_cr": result.cr,
        "ahp_w1": float(result.combined_weight[0]),
        "ahp_w2": float(result.combined_weight[1]),
        "ahp_w3": float(result.combined_weight[2]),
    }


def run_hamiltonian(fig_dir: Path) -> dict[str, float]:
    points = np.array(
        [
            [0.0, 0.0],
            [1.1, 2.0],
            [2.7, 0.4],
            [3.0, 2.7],
            [4.6, 1.1],
            [5.2, 2.9],
        ],
        dtype=float,
    )

    n = len(points)
    graph = np.zeros((n, n), dtype=float)
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            graph[i, j] = float(np.linalg.norm(points[i] - points[j]))

    result = solve_hamiltonian(graph, method="dp")
    plot_hamiltonian_cycle(points, result, output_path=str(fig_dir / "hamiltonian_cycle.png"))

    return {
        "hamiltonian_cost": result.cost,
    }


def run_aco(fig_dir: Path, gif_dir: Path) -> tuple[dict[str, float], np.ndarray, tuple[tuple[int, int], ...]]:
    grid = default_demo_grid(size=32)
    planner = AntColonyPlanner(grid, ACOConfig())
    result = planner.run()

    plot_path_grid(
        grid,
        result.best_path,
        output_path=str(fig_dir / "aco_best_path.png"),
        title=f"ACO Best Path length={result.best_length:.2f}",
    )

    save_aco_path_gif(
        grid,
        result.best_path,
        output_path=str(gif_dir / "aco_path.gif"),
    )

    metrics = {
        "aco_best_length": result.best_length,
    }

    return metrics, grid, result.best_path


def write_summary(root: Path, metrics: dict[str, float]) -> None:
    lines = [
        "# Showcase Metrics",
        "",
        "以下结果由 scripts/build_showcase.py 自动生成。",
        "",
    ]

    for key in sorted(metrics.keys()):
        lines.append(f"- {key}: {metrics[key]:.6f}")

    output = root / "docs" / "results" / "showcase_metrics.md"
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    root = ROOT
    fig_dir, gif_dir = ensure_dirs(root)

    metrics: dict[str, float] = {}
    robotics_metrics, q2_best_history, q2_mean_history, q2_trace = run_robotics(fig_dir, gif_dir)
    metrics.update(robotics_metrics)
    metrics.update(run_ahp(fig_dir))
    metrics.update(run_hamiltonian(fig_dir))

    aco_metrics, aco_grid, aco_path = run_aco(fig_dir, gif_dir)
    metrics.update(aco_metrics)

    save_showcase_cover_gif(
        q2_best_history=q2_best_history,
        q2_mean_history=q2_mean_history,
        q2_trace=q2_trace,
        obstacle_grid=aco_grid,
        aco_path=aco_path,
        output_path=str(gif_dir / "github_cover.gif"),
    )

    write_summary(root, metrics)

    print("Showcase build complete.")
    print(f"Figures: {fig_dir}")
    print(f"GIFs: {gif_dir}")


if __name__ == "__main__":
    main()
