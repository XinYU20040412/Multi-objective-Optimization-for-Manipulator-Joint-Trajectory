"""Static plotting helpers."""

from __future__ import annotations

from typing import Iterable

import matplotlib.pyplot as plt
import numpy as np

from huashu_showcase.ahp import AHPResult
from huashu_showcase.graph import HamiltonianResult
from huashu_showcase.visualization.theme import apply_theme


def _prep_ax(figsize: tuple[float, float] = (8.5, 5.0)):
    apply_theme()
    fig, ax = plt.subplots(figsize=figsize)
    return fig, ax


def plot_ga_history(
    history_best: np.ndarray,
    history_mean: np.ndarray,
    title: str,
    output_path: str,
) -> None:
    fig, ax = _prep_ax((10, 5.5))
    x = np.arange(1, len(history_best) + 1)

    ax.plot(x, history_best, color="#4fe3c1", linewidth=2.4, label="best")
    ax.plot(x, history_mean, color="#f6a623", linewidth=1.8, alpha=0.9, label="mean")
    ax.fill_between(x, history_best, history_mean, color="#4fe3c1", alpha=0.12)

    ax.set_title(title)
    ax.set_xlabel("Generation")
    ax.set_ylabel("Objective value")
    ax.legend(loc="upper right")

    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


def plot_ahp_weights(result: AHPResult, output_path: str) -> None:
    fig, ax = _prep_ax((8.2, 5.0))

    methods = ["Arithmetic", "Geometric", "Eigen", "Combined"]
    matrix = np.vstack(
        [
            result.arithmetic_weight,
            result.geometric_weight,
            result.eigen_weight,
            result.combined_weight,
        ]
    )

    n = matrix.shape[1]
    x = np.arange(n)
    width = 0.18
    colors = ["#6ac9ff", "#ffcc66", "#9cff7f", "#ff7faa"]

    for i, method in enumerate(methods):
        ax.bar(x + (i - 1.5) * width, matrix[i], width=width, label=method, color=colors[i], alpha=0.9)

    ax.set_xticks(x)
    ax.set_xticklabels([f"C{i+1}" for i in range(n)])
    ax.set_ylim(0, max(0.55, float(np.max(matrix)) * 1.25))
    ax.set_title(f"AHP Weights (CR={result.cr:.4f})")
    ax.set_xlabel("Criteria")
    ax.set_ylabel("Weight")
    ax.legend(loc="upper right")

    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


def plot_hamiltonian_cycle(
    points: np.ndarray,
    result: HamiltonianResult,
    output_path: str,
) -> None:
    fig, ax = _prep_ax((7.8, 7.0))
    pts = np.asarray(points, dtype=float)

    ax.scatter(pts[:, 0], pts[:, 1], s=120, color="#67d5ff", edgecolor="#d9f6ff", linewidth=1.0, zorder=4)

    for idx, (x, y) in enumerate(pts):
        ax.text(x + 0.03, y + 0.03, f"N{idx}", fontsize=9, color="#f8fcff", zorder=5)

    cycle = list(result.path)
    for i in range(len(cycle) - 1):
        p1 = pts[cycle[i]]
        p2 = pts[cycle[i + 1]]
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color="#ffb347", linewidth=2.4, alpha=0.9, zorder=3)

    ax.set_title(f"Hamiltonian Cycle ({result.method}) cost={result.cost:.2f}")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_aspect("equal", adjustable="box")

    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


def plot_path_grid(
    obstacle_grid: np.ndarray,
    path: Iterable[tuple[int, int]],
    output_path: str,
    title: str = "ACO Planned Path",
) -> None:
    fig, ax = _prep_ax((7.6, 7.2))
    grid = np.asarray(obstacle_grid)
    ax.imshow(grid, cmap="gray_r", interpolation="nearest")

    coords = np.asarray(list(path), dtype=int)
    if len(coords) > 0:
        ax.plot(coords[:, 1], coords[:, 0], color="#ff5e8a", linewidth=2.6)
        ax.scatter(coords[0, 1], coords[0, 0], color="#62f7b2", s=85, label="start")
        ax.scatter(coords[-1, 1], coords[-1, 0], color="#ffd76a", s=85, label="goal")

    ax.set_title(title)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.legend(loc="upper right")

    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)
