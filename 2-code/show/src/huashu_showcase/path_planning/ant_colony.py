"""Ant Colony Optimization for grid shortest path."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


Coord = tuple[int, int]


@dataclass(frozen=True)
class ACOConfig:
    ants: int = 90
    iterations: int = 120
    alpha: float = 1.1
    beta: float = 4.5
    evaporation: float = 0.2
    deposit_scale: float = 40.0
    seed: int | None = 42


@dataclass(frozen=True)
class ACOResult:
    best_path: tuple[Coord, ...]
    best_length: float
    best_history: np.ndarray
    pheromone: np.ndarray
    explored_paths: list[tuple[Coord, ...]]


class AntColonyPlanner:
    """ACO for 4-neighbor grid path planning with obstacles."""

    def __init__(self, obstacle_grid: np.ndarray, config: ACOConfig) -> None:
        grid = np.asarray(obstacle_grid, dtype=np.uint8)
        if grid.ndim != 2 or grid.shape[0] != grid.shape[1]:
            raise ValueError("obstacle_grid must be a square 2D array")

        self.grid = grid
        self.size = grid.shape[0]
        self.config = config
        self.rng = np.random.default_rng(config.seed)

        self.start: Coord = (0, 0)
        self.goal: Coord = (self.size - 1, self.size - 1)

        if self.grid[self.start] != 0 or self.grid[self.goal] != 0:
            raise ValueError("start and goal cells must be free")

        self.pheromone = np.ones((self.size, self.size), dtype=float)

    @staticmethod
    def _distance(a: Coord, b: Coord) -> float:
        return float(np.hypot(a[0] - b[0], a[1] - b[1]))

    def _neighbors(self, node: Coord) -> list[Coord]:
        x, y = node
        candidates = ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1))
        valid: list[Coord] = []
        for nx, ny in candidates:
            if 0 <= nx < self.size and 0 <= ny < self.size and self.grid[nx, ny] == 0:
                valid.append((nx, ny))
        return valid

    def _path_length(self, path: list[Coord]) -> float:
        if len(path) < 2:
            return float("inf")
        return float(sum(self._distance(path[i], path[i + 1]) for i in range(len(path) - 1)))

    def _construct_one_ant(self) -> tuple[list[Coord], bool]:
        current = self.start
        path = [current]
        visited = {current}
        max_steps = self.size * self.size * 2

        for _ in range(max_steps):
            if current == self.goal:
                return path, True

            neighbors = [n for n in self._neighbors(current) if n not in visited]
            if not neighbors:
                # One-step backtracking for robustness.
                if len(path) > 1:
                    path.pop()
                    current = path[-1]
                    continue
                return path, False

            desirability = []
            for nxt in neighbors:
                tau = self.pheromone[nxt] ** self.config.alpha
                heuristic = 1.0 / (self._distance(nxt, self.goal) + 1e-6)
                eta = heuristic ** self.config.beta
                desirability.append(tau * eta)

            probs = np.asarray(desirability, dtype=float)
            probs /= np.sum(probs)
            idx = int(self.rng.choice(len(neighbors), p=probs))
            current = neighbors[idx]
            path.append(current)
            visited.add(current)

        return path, False

    def _update_pheromone(self, good_paths: list[list[Coord]]) -> None:
        self.pheromone *= 1.0 - self.config.evaporation
        self.pheromone = np.maximum(self.pheromone, 1e-6)

        for path in good_paths:
            length = self._path_length(path)
            if not np.isfinite(length) or length <= 0:
                continue
            delta = self.config.deposit_scale / length
            for node in path:
                self.pheromone[node] += delta

    def run(self) -> ACOResult:
        best_path: list[Coord] = []
        best_length = float("inf")
        best_history: list[float] = []
        explored_paths: list[tuple[Coord, ...]] = []

        for _ in range(self.config.iterations):
            iteration_paths: list[list[Coord]] = []

            for _ in range(self.config.ants):
                path, success = self._construct_one_ant()
                if success:
                    iteration_paths.append(path)
                    explored_paths.append(tuple(path))

                    length = self._path_length(path)
                    if length < best_length:
                        best_length = length
                        best_path = path

            self._update_pheromone(iteration_paths)
            best_history.append(best_length if np.isfinite(best_length) else np.nan)

        if not best_path:
            raise RuntimeError("ACO failed to find a feasible path. Try reducing obstacle density.")

        return ACOResult(
            best_path=tuple(best_path),
            best_length=float(best_length),
            best_history=np.asarray(best_history, dtype=float),
            pheromone=self.pheromone.copy(),
            explored_paths=explored_paths,
        )
