"""Plot theme with a bold GitHub-friendly style."""

from __future__ import annotations

import matplotlib as mpl


def apply_theme() -> None:
    mpl.rcParams.update(
        {
            "figure.facecolor": "#0a0f1f",
            "axes.facecolor": "#11172a",
            "savefig.facecolor": "#0a0f1f",
            "axes.edgecolor": "#d6e2ff",
            "axes.labelcolor": "#e9f1ff",
            "xtick.color": "#e9f1ff",
            "ytick.color": "#e9f1ff",
            "text.color": "#f7fbff",
            "axes.grid": True,
            "grid.color": "#2d3f68",
            "grid.alpha": 0.45,
            "font.size": 11,
            "axes.titleweight": "bold",
            "axes.titlepad": 10,
            "legend.frameon": False,
        }
    )
