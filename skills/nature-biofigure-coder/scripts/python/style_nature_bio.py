"""Matplotlib/seaborn style helpers for biomedical figures."""

from __future__ import annotations

from pathlib import Path

MM_PER_INCH = 25.4


def nature_bio_size_inches(width_class: str = "single", height: float | None = None) -> tuple[float, float]:
    widths_mm = {
        "single": 89,
        "double": 183,
        "extended-data": 180,
    }
    if width_class not in widths_mm:
        raise ValueError(f"Unknown width_class: {width_class}")
    width = widths_mm[width_class] / MM_PER_INCH
    max_height = 170 / MM_PER_INCH
    resolved_height = min(width * 0.75, max_height) if height is None else height
    if resolved_height > max_height:
        raise ValueError("Height exceeds Nature 170 mm maximum.")
    return width, resolved_height


def set_nature_bio_style(base_size: int = 7, font_family: str = "Arial") -> None:
    import matplotlib as mpl
    import seaborn as sns

    if base_size < 5 or base_size > 7:
        raise ValueError("Nature body text should usually be 5-7 pt.")

    sns.set_theme(style="white", context="paper")
    mpl.rcParams.update(
        {
            "font.family": font_family,
            "font.size": base_size,
            "axes.titlesize": base_size,
            "axes.labelsize": base_size,
            "xtick.labelsize": base_size - 1,
            "ytick.labelsize": base_size - 1,
            "legend.fontsize": base_size - 1,
            "axes.linewidth": 0.35,
            "xtick.major.width": 0.35,
            "ytick.major.width": 0.35,
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "savefig.facecolor": "white",
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )


def save_nature_bio_figure(
    fig,
    filename_base: str | Path,
    width_class: str = "single",
    height: float | None = None,
    dpi: int = 450,
    bbox_inches=None,
) -> None:
    base = Path(filename_base)
    width, resolved_height = nature_bio_size_inches(width_class=width_class, height=height)
    fig.set_size_inches(width, resolved_height)
    fig.savefig(base.with_suffix(".pdf"), bbox_inches=bbox_inches)
    fig.savefig(base.with_suffix(".svg"), bbox_inches=bbox_inches)
    fig.savefig(base.with_suffix(".png"), dpi=dpi, bbox_inches=bbox_inches)
