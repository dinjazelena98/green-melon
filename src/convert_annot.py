"""Utility functions to convert Pascal VOC XML format system to YOLO txt format.

In Pascal VOC, the bounding box is defined using absolute pixel values with four coordinates:
    * xmin - The x-coordinate of the top-left corner
    * ymin - The y-coordinate of the top-left corner
    * xmax - The x-coordinate of the bottom-right corner
    * xmin - The y-coordinate of the bottom-right corner
e.g:
<xmin>923</xmin>
<ymin>170</ymin>
<xmax>2066</xmax>
<ymax>1621</ymax>

While for YOLO's annotation format require each object to be presented as single line:
<class_index> <x_center> <y_center> <width> <height>

x_center and y_center - Center of the bounding box
width and height - Dimensions of the bounding box

All these values are normalized by image width and height so values of these coordinates are
between 0 and 1.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET

LABELS_TO_IDS: dict[str, int] = {
    "Alligatorweed": 0,
}


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

    return bndbox_height, bndbox_width, x_center, y_center


def xml2yolo(xml: str, txt: str) -> None:
    """Convert Pascal VOC box format to YOLO box format.

    Args:
    ----
        xml: str -> Path to xml file to convert to txt file.
        txt: str -> Path to text file to write output.

    Returns:
    -------
        list[str]

    """
    yolo_format = []

    tree = ET.parse(xml)  # noqa: S314
    root = tree.getroot()

    # extract image shape
    img_width: int = int(root.find("size").find("width").text)  # type: ignore[union-attr, arg-type]
    img_height: int = int(root.find("size").find("height").text)  # type: ignore[union-attr, arg-type]

    # iterate over all possible objects(bndboxes)
    for obj in root.findall("object"):
        label = obj.find("name").text.strip()  # type: ignore[union-attr]
        if label not in LABELS_TO_IDS:
            raise ValueError(f"{label} not found in {LABELS_TO_IDS.keys()}")  # noqa: TRY003, EM102

        bndbox = obj.find("bndbox")
        xmin = int(bndbox.find("xmin").text)  # type: ignore[union-attr, arg-type]
        ymin = int(bndbox.find("ymin").text)  # type: ignore[union-attr, arg-type]
        xmax = int(bndbox.find("xmax").text)  # type: ignore[union-attr, arg-type]
        ymax = int(bndbox.find("ymax").text)  # type: ignore[union-attr, arg-type]

        bndbox: tuple[float] = convert_bndbox(  # type: ignore[no-redef]
            (img_width, img_height),
            (xmin, ymin, xmax, ymax),
        )
        yolo_format.append(
            f"{LABELS_TO_IDS[label]} " + " ".join(f"{coord:.6f}" for coord in bndbox),  # type: ignore[union-attr]
        )

        with open(txt, "w") as f:  # noqa: PTH123
            f.write("\n".join(yolo_format))


if __name__ == "__main__":
    xml_file: str = "dataset/labels/Alligatorweed (123).xml"
    xml2yolo(xml=xml_file, txt="alligator.txt")
