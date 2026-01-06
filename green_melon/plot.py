"""Module for plotting images with bounding boxes."""

from collections.abc import Iterable
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
from PIL import Image

from green_melon import PascalBbox


def plot_img_with_bboxes(
    image_path: Path, annots: Iterable[tuple[PascalBbox, int]]
) -> tuple[Figure, Axes]:
    """Plot image with bounding boxes."""
    image = Image.open(image_path).convert("RGB")

    fig, ax = plt.subplots(figsize=(15, 12))
    ax.axis("off")
    ax.imshow(image)

    for bbox, target in annots:
        rect = Rectangle(
            (bbox.xmin, bbox.ymin),
            bbox.xmax - bbox.xmin,
            bbox.ymax - bbox.ymin,
            linewidth=1,
            edgecolor="r",
            facecolor="none",
        )
        ax.add_patch(rect)

        ax.text(bbox.xmin, bbox.ymin - 5, f"{target}")
    return fig, ax
