"""
Utility functions to convert Pascal VOC XML format system to YOLO txt format.

In Pascal VOC, the bounding box is defined using absolute pixel values with four coordinates:
    * xmin - The x-coordinate of the top-left corner
    * ymin - The y-coordinate of the top-left corner
    * xmax - The x-coordinate of the bottom-right corner
    * ymax - The y-coordinate of the bottom-right corner
e.g:
<xmin>923</xmin>
<ymin>170</ymin>
<xmax>2066</xmax>
<ymax>1621</ymax>

While YOLO's annotation format requires each object to be presented as a single line:
<class_index> <x_center> <y_center> <width> <height>

x_center and y_center represent the center of the bounding box,
and width and height represent its dimensions.

All these values are normalized by image width and height so that they are between 0 and 1.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path

LABELS_TO_IDS: dict[str, int] = {"Alligatorweed": 0, "Asiatic_Smartweed": 1}


def convert_bndbox(
    size: tuple[int, int],
    bndbox: tuple[int, int, int, int],
) -> tuple[float, float, float, float]:
    """Convert Pascal VOC box format to YOLO box format."""
    img_width, img_height = size
    xmin, ymin, xmax, ymax = bndbox

    bndbox_width: float = (xmax - xmin) / img_width
    bndbox_height: float = (ymax - ymin) / img_height

    x_center: float = (xmin + xmax) / 2 / img_width
    y_center: float = (ymin + ymax) / 2 / img_height

    return x_center, y_center, bndbox_width, bndbox_height


def xml2yolo(xml: str, out: str = "./") -> None:
    """
    Convert Pascal VOC XML format to YOLO txt format.

    Args:
    ----
        xml: Path to xml file to convert.
        out: Directory where to write the YOLO annotation file.
             The output filename will have the same basename as the xml file but with a .txt.

    Returns:
    -------
        None

    """
    yolo_format = []

    tree = ET.parse(xml)  # noqa: S314
    root = tree.getroot()

    img_width: int = int(root.find("size").find("width").text)
    img_height: int = int(root.find("size").find("height").text)
    # iterate over all possible objects(bndboxes)
    for obj in root.findall("object"):
        label = obj.find("name").text.strip()
        if label not in LABELS_TO_IDS:
            msg = f"{label} not found in {LABELS_TO_IDS.keys()}"
            raise ValueError(msg)

        bndbox = obj.find("bndbox")
        xmin = int(bndbox.find("xmin").text)
        ymin = int(bndbox.find("ymin").text)
        xmax = int(bndbox.find("xmax").text)
        ymax = int(bndbox.find("ymax").text)

        yolo_bndbox: tuple[float, float, float, float] = convert_bndbox(
            (img_width, img_height),
            (xmin, ymin, xmax, ymax),
        )
        yolo_format.append(
            f"{LABELS_TO_IDS[label]} " + " ".join(f"{coord:.6f}" for coord in yolo_bndbox),
        )

    with (Path(out) / (Path(xml).stem + ".txt")).open("w") as f:
        f.write("\n".join(yolo_format))
