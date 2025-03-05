"""
Utility Functions for Image Annotation Visualization.

This module provides functions to convert YOLO normalized bounding boxes to absolute pixel
coordinates and to plot annotated images using Pascal VOC (XML), YOLO (TXT), or COCO (JSON) formats.
"""

import json
import xml.etree.ElementTree as ET
from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np

from green_melon.annot import PascalBox, YoloBox, yolo_to_pascal_box


def _draw_annotation(image: np.ndarray, label: str, box: PascalBox) -> None:
    """
    Draw a bounding box and label on the image.

    Args:
    ----
        image (np.ndarray): The image (as a NumPy array) to draw on.
        label (str): The text label to display.
        box (PascalBox): A box with (xmin, ymin, xmax, ymax) coordinates.

    """
    cv2.rectangle(image, (box.xmin, box.ymin), (box.xmax, box.ymax), (255, 0, 0), 5)
    cv2.putText(
        image,
        str(label),
        (box.xmin, max(box.ymin - 10, 0)),  # place of label
        cv2.FONT_HERSHEY_SIMPLEX,  # font
        2,  # scale of font
        (255, 0, 0),  # color
        3,  # thickness
    )


def plot_pascal_img(image_path: str, xml_path: str) -> None:
    """
    Display an image with bounding boxes and labels from a Pascal VOC XML annotation.

    The function reads an image from the `image_path` and parses the associated Pascal VOC XML
    file to extract bounding box coordinates and object names. It then draws the bounding boxes and
    labels on the image.

    Args:
    ----
        image_path (str): Path to the image file.
        xml_path (str): Path to the Pascal VOC XML annotation file.

    Returns:
    -------
        None

    """
    tree = ET.parse(xml_path)  # noqa: S314
    root = tree.getroot()

    image = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)
    for obj in root.findall("object"):
        bndbox = obj.find("bndbox")
        xmin = int(bndbox.find("xmin").text)
        ymin = int(bndbox.find("ymin").text)
        xmax = int(bndbox.find("xmax").text)
        ymax = int(bndbox.find("ymax").text)
        label = obj.find("name").text.strip()
        _draw_annotation(image, label, PascalBox(xmin, ymin, xmax, ymax))

    plt.figure(figsize=(10, 8))
    plt.imshow(image)
    plt.axis("off")
    plt.show()


def plot_yolo_img(image_path: str, txt_path: str) -> None:
    """
    Display an image with bounding boxes and labels from a YOLO TXT annotation.

    The function reads an image from the specified file path and a YOLO annotation from a TXT file.
    Each line in the annotation file should be formatted as:
        <label> <x_center> <y_center> <width> <height>
    where the coordinates are normalized. The function converts these normalized coordinates to
    absolute pixel coordinates and draws the bounding boxes and corresponding label.

    Args:
    ----
        image_path (str): Path to the image file.
        txt_path (str): Path to the YOLO annotation text file.

    Returns:
    -------
        None

    """
    image = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)
    bbox_lines = Path(txt_path).read_text().splitlines()

    for line in bbox_lines:
        parts = line.split()
        label = int(parts[0])
        x_center = float(parts[1])
        y_center = float(parts[2])
        width = float(parts[3])
        height = float(parts[4])

        xmin, ymin, xmax, ymax = yolo_to_pascal_box(
            (image.shape[1], image.shape[0]), YoloBox(x_center, y_center, width, height)
        )
        _draw_annotation(image, str(label), PascalBox(xmin, ymin, xmax, ymax))

    plt.figure(figsize=(10, 8))
    plt.imshow(image)
    plt.axis("off")
    plt.show()


def plot_coco_img(image_path: str, json_path: str) -> None:
    """
    Display an image with bounding boxes and labels from a COCO JSON annotation.

    The function reads an image from the specified file path and a COCO annotation from a JSON file.
    Each bbox in the annotation file should be formatted as: [x, y, width, height].

    Args:
    ----
        image_path (str): Path to the image file.
        json_path (str): Path to the COCO annotation JSON file.

    Returns:
    -------
        None

    """
    with Path(json_path).open() as f:
        coco_annotations = json.load(f)

    # Create a mapping from image file names to their image info.
    image_info_map: dict[str, dict] = {
        img_info["file_name"]: img_info for img_info in coco_annotations["images"]
    }
    current_image_id = image_info_map[Path(image_path).name]["id"]

    # Filter annotations corresponding to the current image using its image ID.
    current_image_annotations = [
        ann for ann in coco_annotations["annotations"] if ann["image_id"] == current_image_id
    ]

    image = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)

    for annotation in current_image_annotations:
        x_min, y_min, bbox_width, bbox_height = annotation["bbox"]
        x_max = x_min + bbox_width
        y_max = y_min + bbox_height

        _draw_annotation(
            image, str(annotation["category_id"]), PascalBox(x_min, y_min, x_max, y_max)
        )

    plt.figure(figsize=(10, 8))
    plt.imshow(image)
    plt.axis("off")
    plt.show()
