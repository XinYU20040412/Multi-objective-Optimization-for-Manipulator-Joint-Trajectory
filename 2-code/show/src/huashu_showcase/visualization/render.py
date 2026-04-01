"""Animation rendering helpers (GIF)."""

from __future__ import annotations

from io import BytesIO
from math import cos, pi, sin

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from huashu_showcase.config import ArmConfig, DEFAULT_ARM_CONFIG
from huashu_showcase.robotics.model import denormalize_angles_rad, endpoint_mm
from huashu_showcase.visualization.theme import apply_theme


def _fig_to_pil(fig: plt.Figure, dpi: int = 150) -> Image.Image:
    buffer = BytesIO()
    fig.savefig(buffer, format="png", dpi=dpi, bbox_inches="tight")
    plt.close(fig)
    buffer.seek(0)
    return Image.open(buffer).convert("RGB")


def _sample_indices(total: int, max_frames: int) -> list[int]:
    if total <= 0:
        return []
    if total == 1:
        return [0]

    stride = max(1, total // max_frames)
    sampled = list(range(0, total, stride))
    if sampled[-1] != total - 1:
        sampled.append(total - 1)
    return sampled


def _robot_chain_points_mm(norm_params: np.ndarray, config: ArmConfig) -> np.ndarray:
    a1, a2, _ = denormalize_angles_rad(norm_params)

    p0 = np.array([0.0, 0.0, 0.0], dtype=float)
    p1 = np.array([0.0, 0.0, config.base_height_mm], dtype=float)
    p2 = np.array(
        [
            config.link1_mm * cos(a1),
            config.link1_mm * sin(a1),
            config.base_height_mm,
        ],
        dtype=float,
    )

    x_local = config.link2_mm * cos(a2 + pi / 2.0)
    y_local = config.link2_mm * sin(a2 + pi / 2.0)
    p3 = np.array(
        [
            p2[0] + cos(a1) * x_local,
            p2[1] + sin(a1) * x_local,
            config.base_height_mm + y_local,
        ],
        dtype=float,
    )

    p4 = endpoint_mm(norm_params, config)
    return np.vstack([p0, p1, p2, p3, p4])


def save_robotics_grasp_2d3d_gif(
    best_trace: np.ndarray,
    output_path: str,
    fps: int = 14,
    max_frames: int = 64,
    config: ArmConfig = DEFAULT_ARM_CONFIG,
) -> None:
    """Export a side-by-side 2D/3D robot grasp animation from GA best-trace."""

    apply_theme()
    trace = np.asarray(best_trace, dtype=float)
    if trace.ndim != 2 or trace.shape[1] != 3:
        raise ValueError("best_trace must have shape (n_generations, 3)")

    sampled_idx = _sample_indices(len(trace), max_frames)
    if not sampled_idx:
        raise ValueError("No frame generated for robotics GIF")

    target = np.asarray(config.target_mm, dtype=float)
    max_reach = config.link1_mm + config.link2_mm + config.link3_mm + 220.0
    z_max = config.base_height_mm + config.link2_mm + config.link3_mm + 260.0

    frames: list[Image.Image] = []
    for frame_id, idx in enumerate(sampled_idx):
        progress = frame_id / max(len(sampled_idx) - 1, 1)

        fig = plt.figure(figsize=(11.2, 5.5))
        gs = fig.add_gridspec(1, 2, width_ratios=[1.02, 1.08], wspace=0.14)

        ax2d = fig.add_subplot(gs[0, 0])
        ax3d = fig.add_subplot(gs[0, 1], projection="3d")

        chain = _robot_chain_points_mm(trace[idx], config)
        hist_ids = sampled_idx[: frame_id + 1]
        endpoint_hist = np.asarray([endpoint_mm(trace[i], config) for i in hist_ids], dtype=float)
        dist = float(np.linalg.norm(chain[-1] - target))

        # Left panel: 2D top view for planar grasp trajectory.
        ax2d.plot(endpoint_hist[:, 0], endpoint_hist[:, 1], color="#5de2ff", linewidth=1.8, alpha=0.75, label="gripper path")
        ax2d.plot(chain[:, 0], chain[:, 1], color="#ffb870", linewidth=3.0, marker="o", markersize=5.0, label="arm chain")
        ax2d.scatter(target[0], target[1], color="#67f9b8", marker="*", s=130, label="target")
        ax2d.scatter(chain[-1, 0], chain[-1, 1], color="#ff4f87", s=60, zorder=6, label="gripper")

        ax2d.set_title("Mechanical Arm Grasp (2D Top View)")
        ax2d.set_xlabel("x (mm)")
        ax2d.set_ylabel("y (mm)")
        ax2d.set_xlim(-max_reach, max_reach)
        ax2d.set_ylim(-max_reach, max_reach)
        ax2d.set_aspect("equal", adjustable="box")
        ax2d.legend(loc="upper right")

        # Right panel: 3D joint-control motion for premium showcase feel.
        ax3d.plot(chain[:, 0], chain[:, 1], chain[:, 2], color="#f6a623", linewidth=3.1, marker="o", markersize=4.8)
        ax3d.plot(endpoint_hist[:, 0], endpoint_hist[:, 1], endpoint_hist[:, 2], color="#73f0ff", linewidth=1.4, alpha=0.8)
        ax3d.scatter(target[0], target[1], target[2], color="#67f9b8", marker="*", s=140)
        ax3d.scatter(chain[-1, 0], chain[-1, 1], chain[-1, 2], color="#ff4f87", s=62)

        ax3d.set_title("Mechanical Arm Grasp (3D Joint Control)")
        ax3d.set_xlabel("x (mm)")
        ax3d.set_ylabel("y (mm)")
        ax3d.set_zlabel("z (mm)")
        ax3d.set_xlim(-max_reach, max_reach)
        ax3d.set_ylim(-max_reach, max_reach)
        ax3d.set_zlim(0.0, z_max)
        ax3d.view_init(elev=23.0 + 4.0 * np.sin(2.0 * pi * progress), azim=-62.0 + 24.0 * progress)

        for axis in (ax3d.xaxis, ax3d.yaxis, ax3d.zaxis):
            axis.pane.set_facecolor((0.07, 0.11, 0.20, 1.0))
            axis.pane.set_edgecolor((0.24, 0.33, 0.50, 1.0))

        fig.suptitle("Robot Arm Optimization Showcase", fontsize=19, fontweight="bold")
        fig.text(
            0.5,
            0.02,
            (
                f"Gen {idx + 1:03d}/{len(trace):03d}"
                f" | target=({target[0]:.0f}, {target[1]:.0f}, {target[2]:.0f}) mm"
                f" | dist={dist:.2f} mm"
            ),
            ha="center",
            va="bottom",
            fontsize=11,
            color="#d9e8ff",
        )

        fig.tight_layout(rect=(0.0, 0.04, 1.0, 0.97))
        frames.append(_fig_to_pil(fig, dpi=118))

    duration = int(1000 / max(fps, 1))
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=duration,
        loop=0,
        optimize=False,
    )


def save_ga_evolution_gif(best_trace: np.ndarray, output_path: str, fps: int = 15) -> None:
    apply_theme()
    trace = np.asarray(best_trace, dtype=float)
    if trace.ndim != 2 or trace.shape[1] != 3:
        raise ValueError("best_trace must have shape (n_generations, 3)")

    frames: list[Image.Image] = []

    # Subsample long traces to keep GIF size practical.
    sampled_idx = _sample_indices(len(trace), 90)

    for idx in sampled_idx:
        fig, ax = plt.subplots(figsize=(7.8, 4.7))

        x = np.arange(idx + 1)
        ax.plot(x, trace[: idx + 1, 0], color="#5de2ff", linewidth=2.2, label="joint-1")
        ax.plot(x, trace[: idx + 1, 1], color="#ffb870", linewidth=2.2, label="joint-2")
        ax.plot(x, trace[: idx + 1, 2], color="#96ff8d", linewidth=2.2, label="joint-3")

        # Mark current frame point to avoid a visually empty first frame.
        ax.scatter([idx], [trace[idx, 0]], color="#5de2ff", s=28, zorder=4)
        ax.scatter([idx], [trace[idx, 1]], color="#ffb870", s=28, zorder=4)
        ax.scatter([idx], [trace[idx, 2]], color="#96ff8d", s=28, zorder=4)

        ax.set_title("GA Evolution Trace (Best Individual)")
        ax.set_xlabel("Generation")
        ax.set_ylabel("Normalized parameter")
        ax.set_ylim(-0.02, 1.02)
        ax.set_xlim(0, max(1, len(trace) - 1))
        ax.legend(loc="upper right")
        ax.grid(True, alpha=0.35)

        frames.append(_fig_to_pil(fig))

    if not frames:
        raise ValueError("No frame generated for GA GIF")

    duration = int(1000 / max(fps, 1))
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=duration,
        loop=0,
        optimize=False,
    )


def save_showcase_cover_gif(
    q2_best_history: np.ndarray,
    q2_mean_history: np.ndarray,
    q2_trace: np.ndarray,
    obstacle_grid: np.ndarray,
    aco_path: tuple[tuple[int, int], ...],
    output_path: str,
    fps: int = 14,
) -> None:
    """Create a high-impact GitHub cover GIF with multi-algorithm storytelling."""

    apply_theme()

    q2_best_history = np.asarray(q2_best_history, dtype=float).reshape(-1)
    q2_mean_history = np.asarray(q2_mean_history, dtype=float).reshape(-1)
    q2_trace = np.asarray(q2_trace, dtype=float)
    obstacle_grid = np.asarray(obstacle_grid)
    coords = np.asarray(aco_path, dtype=int)

    if q2_trace.ndim != 2 or q2_trace.shape[1] != 3:
        raise ValueError("q2_trace must have shape (n_generations, 3)")
    if q2_best_history.size == 0 or q2_mean_history.size == 0:
        raise ValueError("q2 histories cannot be empty")
    if coords.size == 0:
        raise ValueError("aco_path cannot be empty")

    n_frames = max(
        len(_sample_indices(len(q2_best_history), 78)),
        len(_sample_indices(len(coords), 78)),
    )
    n_frames = max(n_frames, 24)

    frames: list[Image.Image] = []
    for frame_idx in range(n_frames):
        progress = frame_idx / max(n_frames - 1, 1)

        ga_end = max(1, int(round(progress * (len(q2_best_history) - 1))) + 1)
        if len(coords) > 1:
            path_end = max(2, int(round(progress * (len(coords) - 1))) + 1)
        else:
            path_end = 1

        fig = plt.figure(figsize=(12.6, 7.2))
        gs = fig.add_gridspec(2, 2, width_ratios=[1.55, 1.0], height_ratios=[1.0, 1.0], wspace=0.12, hspace=0.16)

        ax_conv = fig.add_subplot(gs[0, 0])
        ax_trace = fig.add_subplot(gs[1, 0])
        ax_path = fig.add_subplot(gs[:, 1])

        # Panel 1: objective convergence.
        x = np.arange(1, ga_end + 1)
        ax_conv.plot(x, q2_best_history[:ga_end], color="#4fe3c1", linewidth=2.4, label="best")
        ax_conv.plot(x, q2_mean_history[:ga_end], color="#f6a623", linewidth=2.0, label="mean")
        ax_conv.fill_between(x, q2_best_history[:ga_end], q2_mean_history[:ga_end], color="#4fe3c1", alpha=0.10)
        ax_conv.scatter([ga_end], [q2_best_history[ga_end - 1]], color="#ff5e8a", s=40, zorder=5)
        ax_conv.set_xlim(1, len(q2_best_history))
        ax_conv.set_title("Question 2 Convergence")
        ax_conv.set_xlabel("Generation")
        ax_conv.set_ylabel("Objective")
        ax_conv.legend(loc="upper right")

        # Panel 2: best-individual parameter trajectory.
        tx = np.arange(ga_end)
        ax_trace.plot(tx, q2_trace[:ga_end, 0], color="#5de2ff", linewidth=2.2, label="joint-1")
        ax_trace.plot(tx, q2_trace[:ga_end, 1], color="#ffb870", linewidth=2.2, label="joint-2")
        ax_trace.plot(tx, q2_trace[:ga_end, 2], color="#96ff8d", linewidth=2.2, label="joint-3")
        ax_trace.scatter([ga_end - 1], [q2_trace[ga_end - 1, 0]], color="#5de2ff", s=24)
        ax_trace.scatter([ga_end - 1], [q2_trace[ga_end - 1, 1]], color="#ffb870", s=24)
        ax_trace.scatter([ga_end - 1], [q2_trace[ga_end - 1, 2]], color="#96ff8d", s=24)
        ax_trace.set_ylim(-0.02, 1.02)
        ax_trace.set_xlim(0, max(1, len(q2_trace) - 1))
        ax_trace.set_title("Best Individual Trace")
        ax_trace.set_xlabel("Generation")
        ax_trace.set_ylabel("Normalized value")
        ax_trace.legend(loc="upper right")

        # Panel 3: ACO path expansion on obstacle map.
        ax_path.imshow(obstacle_grid, cmap="gray_r", interpolation="nearest")
        path_segment = coords[:path_end]
        ax_path.plot(path_segment[:, 1], path_segment[:, 0], color="#ff4f87", linewidth=2.8)
        ax_path.scatter(path_segment[0, 1], path_segment[0, 0], color="#67f9b8", s=90, label="start")
        ax_path.scatter(coords[-1, 1], coords[-1, 0], color="#ffd66b", s=90, label="goal")
        ax_path.set_title("ACO Path Expansion")
        ax_path.set_xticks([])
        ax_path.set_yticks([])
        ax_path.legend(loc="upper right")

        fig.suptitle("Huashu Cup Algorithm Showcase", fontsize=20, fontweight="bold")
        fig.text(
            0.5,
            0.018,
            f"GA Gen {ga_end:03d} | Best={q2_best_history[ga_end - 1]:.4f} | ACO Steps={path_end}/{len(coords)}",
            ha="center",
            va="bottom",
            fontsize=11,
            color="#d9e8ff",
        )

        frames.append(_fig_to_pil(fig))

    duration = int(1000 / max(fps, 1))
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=duration,
        loop=0,
        optimize=False,
    )


def save_aco_path_gif(
    obstacle_grid: np.ndarray,
    path: tuple[tuple[int, int], ...],
    output_path: str,
    fps: int = 16,
) -> None:
    apply_theme()
    grid = np.asarray(obstacle_grid)
    coords = np.asarray(path, dtype=int)
    frames: list[Image.Image] = []

    if len(coords) == 0:
        raise ValueError("Path is empty")

    for end_idx in range(2, len(coords) + 1):
        fig, ax = plt.subplots(figsize=(7.2, 7.0))
        ax.imshow(grid, cmap="gray_r", interpolation="nearest")

        segment = coords[:end_idx]
        ax.plot(segment[:, 1], segment[:, 0], color="#ff4f87", linewidth=2.8)
        ax.scatter(segment[0, 1], segment[0, 0], color="#67f9b8", s=90)
        ax.scatter(coords[-1, 1], coords[-1, 0], color="#ffd66b", s=90)

        ax.set_title("ACO Path Expansion")
        ax.set_xticks([])
        ax.set_yticks([])
        ax.grid(False)

        frames.append(_fig_to_pil(fig))

    duration = int(1000 / max(fps, 1))
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=duration,
        loop=0,
        optimize=False,
    )
