"""
Utility functions to convert between Pascal VOC XML annotations and YOLO TXT format.

Pascal VOC uses pixel coordinates (xmin, ymin, xmax, ymax), while YOLO uses normalized
coordinates (<class_index> <x_center> <y_center> <width> <height>).
"""

from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterator


@dataclass
class PascalBox:
    """
    Represents a bounding box in Pascal VOC format.

    Attributes
    ----------
        xmin (int): The x-coordinate of the top-left corner in pixels.
        ymin (int): The y-coordinate of the top-left corner in pixels.
        xmax (int): The x-coordinate of the bottom-right corner in pixels.
        ymax (int): The y-coordinate of the bottom-right corner in pixels.

    """

    xmin: int
    ymin: int
    xmax: int
    ymax: int

    def __iter__(self) -> Iterator[int]:
        """
        Iterate over the bounding box coordinates.

        Yields
        ------
            Iterator[int]: Coordinates in the order: xmin, ymin, xmax, ymax.

        """
        return iter((self.xmin, self.ymin, self.xmax, self.ymax))


@dataclass
class YoloBox:
    """
    Represents a bounding box in YOLO format with normalized coordinates.

    Attributes
    ----------
        x_center (float): The normalized x-coordinate of the box center (value between 0 and 1).
        y_center (float): The normalized y-coordinate of the box center (value between 0 and 1).
        bbox_width (float): The normalized width of the bounding box (value between 0 and 1).
        bbox_height (float): The normalized height of the bounding box (value between 0 and 1).

    """

    x_center: float
    y_center: float
    bbox_width: float
    bbox_height: float

    def __iter__(self) -> Iterator[float]:
        """
        Iterate over the YOLO bounding box parameters.

        Yields
        ------
            Iterator[float]: Parameters in the order: x_center, y_center, bbox_width, bbox_height.

        """
        return iter((self.x_center, self.y_center, self.bbox_width, self.bbox_height))


def pascal_to_yolo_box(
    size: tuple[int, int],
    bbox: PascalBox,
) -> YoloBox:
    """
    Convert a Pascal VOC bounding box to YOLO format.

    Args:
    ----
        size (tuple[int, int]): The dimensions of the image in pixels (width, height).
        bbox (PascalBox): The bounding box in Pascal VOC format.

    Returns:
    -------
        YoloBox: The bounding box in YOLO format with normalized coordinates:
            - x_center: normalized center x-coordinate,
            - y_center: normalized center y-coordinate,
            - bbox_width: normalized width,
            - bbox_height: normalized height.

    """
    img_width, img_height = size

    bndbox_width: float = (bbox.xmax - bbox.xmin) / img_width
    bndbox_height: float = (bbox.ymax - bbox.ymin) / img_height
    x_center: float = (bbox.xmin + bbox.xmax) / 2 / img_width
    y_center: float = (bbox.ymin + bbox.ymax) / 2 / img_height

    return YoloBox(x_center, y_center, bndbox_width, bndbox_height)


def yolo_to_pascal_box(size: tuple[int, int], bbox: YoloBox) -> PascalBox:
    """
    Convert a YOLO bounding box to Pascal VOC format.

    Args:
    ----
        size (tuple[int, int]): The dimensions of the image in pixels (width, height).
        bbox (YoloBox): The bounding box in YOLO format with normalized coordinates.

    Returns:
    -------
        PascalBox: The bounding box in Pascal VOC format, where:
            - xmin and ymin are the pixel coordinates of the top-left corner,
            - xmax and ymax are the pixel coordinates of the bottom-right corner.

    """
    img_width, img_height = size

    x_max: float = img_width * bbox.x_center + (bbox.bbox_width * img_width / 2)
    x_min: float = img_width * bbox.x_center - (bbox.bbox_width * img_width / 2)
    y_max: float = img_height * bbox.y_center + (bbox.bbox_height * img_height / 2)
    y_min: float = img_height * bbox.y_center - (bbox.bbox_height * img_height / 2)

    return PascalBox(int(round(x_min)), int(round(y_min)), int(round(x_max)), int(round(y_max)))


def xml2yolo(xml_path: str, labels_mapping: dict[str, int], out: str = "./") -> None:
    """
    Convert a Pascal VOC XML annotation file to YOLO TXT format.

    Args:
    ----
        xml_path (str): The path to the XML file to convert.
        labels_mapping (dict[str, int]): A dictionary mapping class names to YOLO class indices.
        out (str, optional): The directory where the YOLO annotation file will be saved.
            The output file will have the same base name as the XML file with a .txt extension.

    Returns:
    -------
        None

    """
    yolo_format = []

    tree = ET.parse(xml_path)  # noqa: S314
    root = tree.getroot()

    img_width: int = int(root.find("size").find("width").text)
    img_height: int = int(root.find("size").find("height").text)

    for obj in root.findall("object"):
        label = obj.find("name").text.strip()
        if label not in labels_mapping:
            msg = f"{label} not found in {list(labels_mapping.keys())}"
            raise ValueError(msg)

        bndbox = obj.find("bndbox")
        xmin = int(bndbox.find("xmin").text)
        ymin = int(bndbox.find("ymin").text)
        xmax = int(bndbox.find("xmax").text)
        ymax = int(bndbox.find("ymax").text)

        yolo_bndbox: YoloBox = pascal_to_yolo_box(
            (img_width, img_height),
            PascalBox(xmin, ymin, xmax, ymax),
        )
        yolo_format.append(
            f"{labels_mapping[label]} " + " ".join(f"{coord:.6f}" for coord in yolo_bndbox)
        )

    out_path = Path(out)
    out_path.mkdir(parents=True, exist_ok=True)
    output_file = out_path / (Path(xml_path).stem + ".txt")
    with output_file.open("w") as f:
        f.write("\n".join(yolo_format))


def json2yolo(json_path: str, labels_mapping: dict, out: str = "./") -> None:
    """
    Convert COCO annotations to YOLO TXT format and save them to text files.

    This function reads a COCO-format JSON file containing image and annotation data,
    converts each annotation's bounding box into YOLO format
    (normalized x_center, y_center, width, height), and writes the annotations for each image into
    a separate text file in the specified output directory.
    The YOLO label for each annotation is determined using the provided labels_mapping dictionary.

    Args:
    ----
        json_path (str): The file path to the input JSON file in COCO format.
        labels_mapping (dict): A mapping from COCO category IDs to YOLO label indices.
        out (str, optional): The output directory where YOLO-format annotation files will be saved.
            Defaults to "./".

    Returns:
    -------
        None

    """
    with Path(json_path).open("r") as f:
        coco_annotations = json.load(f)

    annots_per_img: dict = {}
    # Key is image_id, values are list of annotations(bbox, label_id) for given image

    for annot in coco_annotations["annotations"]:
        annots_per_img.setdefault(annot["image_id"], []).append(annot)

    imgs_per_id: dict[str, dict] = {img["id"]: img for img in coco_annotations["images"]}
    # Key is image_id, value is image info, e.g height, width
    for img_id, img in imgs_per_id.items():
        img_width: int = img["width"]
        img_height: int = img["height"]

        yolo_coordinates = []

        for annot in annots_per_img[img_id]:
            x, y, bbox_width, bbox_height = annot["bbox"]

            x_center: float = (x + bbox_width / 2.0) / img_width
            y_center: float = (y + bbox_height / 2.0) / img_height
            bbox_width /= img_width
            bbox_height /= img_height

            yolo_label = labels_mapping[annot["category_id"]]

            yolo_coordinates.append(
                f"{yolo_label} {x_center:.6f} {y_center:.6f} {bbox_width:.6f} {bbox_height:.6f}"
            )
        output_file: Path = Path(out) / (Path(img["file_name"]).stem + ".txt")
        with output_file.open("w") as f:
            f.write("\n".join(yolo_coordinates))
