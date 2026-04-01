"""Fast command for updating only GitHub cover GIF."""

# pyright: reportMissingImports=false

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from huashu_showcase.robotics import run_question2
from huashu_showcase.path_planning import ACOConfig, AntColonyPlanner, default_demo_grid
from huashu_showcase.visualization import save_robotics_grasp_2d3d_gif, save_showcase_cover_gif


def main() -> None:
    root = ROOT
    gif_dir = root / "assets" / "gifs"
    gif_dir.mkdir(parents=True, exist_ok=True)

    result = run_question2()
    grid = default_demo_grid(size=32)
    aco_result = AntColonyPlanner(grid, ACOConfig()).run()

    out = gif_dir / "github_cover.gif"
    save_showcase_cover_gif(
        q2_best_history=result.ga_result.history_best,
        q2_mean_history=result.ga_result.history_mean,
        q2_trace=result.ga_result.best_trace,
        obstacle_grid=grid,
        aco_path=aco_result.best_path,
        output_path=str(out),
    )
    save_robotics_grasp_2d3d_gif(
        result.ga_result.best_trace,
        output_path=str(gif_dir / "robotics_grasp_2d3d.gif"),
    )
    print(f"Updated cover GIF: {out}")


if __name__ == "__main__":
    main()
