"""Grid utilities for ACO path planning."""

from __future__ import annotations

import numpy as np


def random_obstacle_grid(
    size: int = 30,
    obstacle_ratio: float = 0.2,
    seed: int = 42,
) -> np.ndarray:
    if not 0.0 <= obstacle_ratio < 0.6:
        raise ValueError("obstacle_ratio must be in [0.0, 0.6)")

    rng = np.random.default_rng(seed)
    grid = (rng.random((size, size)) < obstacle_ratio).astype(np.uint8)

    # Keep start and goal open.
    grid[0, 0] = 0
    grid[size - 1, size - 1] = 0

    # Carve a loose diagonal corridor to avoid disconnected maps.
    for i in range(size):
        grid[i, i] = 0
        if i + 1 < size:
            grid[i + 1, i] = 0

    return grid


def default_demo_grid(size: int = 32) -> np.ndarray:
    grid = random_obstacle_grid(size=size, obstacle_ratio=0.22, seed=2026)

    # Add a geometric obstacle pattern to make the visualization richer.
    grid[size // 4 : size // 4 + 2, 2 : size - 2] = 1
    grid[size // 2 : size // 2 + 2, 3 : size - 3] = 1
    grid[3 : size - 3, size // 3 : size // 3 + 2] = 1

    grid[0, 0] = 0
    grid[size - 1, size - 1] = 0
    grid[size // 4, size // 2] = 0
    grid[size // 2, size // 4] = 0
    return grid
