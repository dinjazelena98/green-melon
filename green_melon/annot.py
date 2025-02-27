"""
Utility functions to convert between Pascal VOC XML annotations and YOLO TXT format.

Pascal VOC uses pixel coordinates (xmin, ymin, xmax, ymax), while YOLO uses normalized
coordinates (<class_index> <x_center> <y_center> <width> <height>).
"""

from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from pathlib import Path


def pascal_to_yolo_box(
    size: tuple[int, int],
    bndbox: tuple[int, int, int, int],
) -> tuple[float, float, float, float]:
    """
    Convert a Pascal VOC bounding box to YOLO format.

    Args:
    ----
        size: (width, height) of the image in pixels.
        bndbox: Bounding box as (xmin, ymin, xmax, ymax).

    Returns:
    -------
        Bounding box in YOLO format as (x_center, y_center, width, height) with values normalized.

    """
    img_width, img_height = size
    xmin, ymin, xmax, ymax = bndbox

    bndbox_width: float = (xmax - xmin) / img_width
    bndbox_height: float = (ymax - ymin) / img_height
    x_center: float = (xmin + xmax) / 2 / img_width
    y_center: float = (ymin + ymax) / 2 / img_height

    return x_center, y_center, bndbox_width, bndbox_height


def yolo_to_pascal_box(
    yolo_coordinates: tuple[float, float, float, float], image_size: tuple[int, int]
) -> tuple[int, int, int, int]:
    """
    Convert YOLO bounding box coordinates to Pascal VOC format.

    Args:
    ----
        yolo_coordinates: (x_center, y_center, width, height) in normalized values.
        image_size: (width, height) of the image in pixels.

    Returns:
    -------
        Bounding box in Pascal VOC format as (xmin, ymin, xmax, ymax) in pixel values.

    """
    x_center, y_center, box_width, box_height = yolo_coordinates
    img_width, img_height = image_size

    x_max: float = img_width * x_center + (box_width * img_width / 2)
    x_min: float = img_width * x_center - (box_width * img_width / 2)
    y_max: float = img_height * y_center + (box_height * img_height / 2)
    y_min: float = img_height * y_center - (box_height * img_height / 2)

    return int(x_min), int(y_min), int(x_max), int(y_max)


def xml2yolo(xml_path: str, labels_mapping: dict[str, int], out: str = "./") -> None:
    """
    Convert Pascal VOC XML format to YOLO txt format.

    Args:
    ----
        xml_path: Path to xml file to convert.
        labels_mapping: A dictionary mapping class names (str) to YOLO class indices (int).
        out: Directory where to write the YOLO annotation file.
             The output filename will have the same basename as the xml file but with a .txt.

    Returns:
    -------
        None

    """
    yolo_format = []

    tree = ET.parse(xml_path)  # noqa: S314
    root = tree.getroot()

    img_width: int = int(root.find("size").find("width").text)
    img_height: int = int(root.find("size").find("height").text)
    # iterate over all possible objects(bndboxes)
    for obj in root.findall("object"):
        label = obj.find("name").text.strip()
        if label not in labels_mapping:
            msg = f"{label} not found in {labels_mapping.keys()}"
            raise ValueError(msg)

        bndbox = obj.find("bndbox")
        xmin = int(bndbox.find("xmin").text)
        ymin = int(bndbox.find("ymin").text)
        xmax = int(bndbox.find("xmax").text)
        ymax = int(bndbox.find("ymax").text)

        yolo_bndbox: tuple[float, float, float, float] = pascal_to_yolo_box(
            (img_width, img_height),
            (xmin, ymin, xmax, ymax),
        )
        yolo_format.append(
            f"{labels_mapping[label]} " + " ".join(f"{coord:.6f}" for coord in yolo_bndbox),
        )

    out_path = Path(out)
    out_path.mkdir(parents=True, exist_ok=True)
    output_file = out_path / (Path(xml_path).stem + ".txt")
    with output_file.open("w") as f:
        f.write("\n".join(yolo_format))


def coco_to_yolo_box(json_path: str, labels_mapping: dict, out: str = "./") -> None:
    """
    Convert COCO annotations to YOLO format and save them to text files.

    This function reads a COCO-format JSON file containing image and annotation data,
    converts each annotation's bounding box into the YOLO format (normalized x_center,
    y_center, width, height), and writes the annotations for each image into a separate
    text file in the specified output directory. The YOLO label for each annotation is
    determined using the provided labels_mapping dictionary.

    Args:
    ----
        json_path (str): The file path to the input JSON file in COCO format.
        labels_mapping (dict): A mapping from COCO category IDs to YOLO label indices.
        out (str, optional): The output directory where YOLO-format annotation files will be saved.
                             Defaults to "./".

    """
    with Path(json_path).open("r") as f:
        annotations = json.load(f)

    annots_per_img: dict = {}
    for annot in annotations["annotations"]:
        annots_per_img.setdefault(annot["image_id"], []).append(annot)

    imgs_to_ids: dict[str, dict] = {img["id"]: img for img in annotations["images"]}

    for img_id, img in imgs_to_ids.items():
        img_width: int = img["width"]
        img_height: int = img["height"]

        coordinates = []

        for annot in annots_per_img[img_id]:
            x, y, bbox_width, bbox_height = annot["bbox"]

            x_center: float = (x + bbox_width / 2.0) / img_width
            y_center: float = (y + bbox_height / 2.0) / img_height
            bbox_width /= img_width
            bbox_height /= img_height

            yolo_label = labels_mapping.get(annot["category_id"], -1)

            coordinates.append(
                f"{yolo_label} {x_center:.6f} {y_center:.6f} {bbox_width:.6f} {bbox_height:.6f}"
            )
        output_file: Path = Path(out) / (Path(img["file_name"]).stem + ".txt")
        with output_file.open("w") as f:
            f.write("\n".join(coordinates))
