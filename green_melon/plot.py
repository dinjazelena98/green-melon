"""
Utility Functions for Image Annotation Visualization.

This module provides functions to convert YOLO normalized bounding boxes to absolute pixel
coordinates and to plot annotated images using either Pascal VOC (XML) or YOLO (TXT) formats.
"""

import xml.etree.ElementTree as ET
from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np

from green_melon.annot import yolo_to_pascal_box


def _draw_annotation(
    image: np.ndarray,
    label: str,
    box: tuple[int, int, int, int],
) -> None:
    """
    Draw a bounding box and label on the image.

    Args:
    ----
        image: The image (as a NumPy array) to draw on.
        label: The text label to display.
        box: A tuple (xmin, ymin, xmax, ymax) defining the bounding box.

    """
    xmin, ymin, xmax, ymax = box
    cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (255, 0, 0), 5)
    cv2.putText(
        image,
        label,
        (xmin, max(ymin - 10, 0)),
        cv2.FONT_HERSHEY_SIMPLEX,
        2,
        (255, 0, 0),
        3,
    )


def plot_pascal_img(img: str, xml: str) -> None:
    """
    Display an image with bounding boxes and labels from a Pascal VOC XML annotation.

    The function reads an image from the specified file path and parses the associated Pascal VOC XML
    file to extract bounding box coordinates and object names. It then draws the bounding boxes and
    labels on the image.

    Args:
    ----
        img (str):
            Path to the image file.
        xml (str):
            Path to the Pascal VOC XML annotation file.

    Returns:
    -------
        None

    """  # noqa: E501
    tree = ET.parse(xml)  # noqa: S314
    root = tree.getroot()

    image = cv2.cvtColor(cv2.imread(img), cv2.COLOR_BGR2RGB)

    for obj in root.findall("object"):
        bndbox = obj.find("bndbox")

        xmin = int(bndbox.find("xmin").text)
        ymin = int(bndbox.find("ymin").text)
        xmax = int(bndbox.find("xmax").text)
        ymax = int(bndbox.find("ymax").text)

        _draw_annotation(image, obj.find("name").text.strip(), (xmin, ymin, xmax, ymax))

    plt.figure(figsize=(10, 8))
    plt.imshow(image)
    plt.axis("off")
    plt.show()


def plot_yolo_img(img: str, txt: str) -> None:
    """
    Display an image with bounding boxes and labels from a YOLO TXT annotation.

    The function reads an image from the specified file path and a YOLO annotation from a TXT file.
    Each line in the annotation file should be formatted as:
        <label> <x_center> <y_center> <width> <height>
    where the coordinates are normalized. The function converts these normalized coordinates to
    absolute pixel coordinates and draws the bounding boxes and corresponding label.

    Args:
    ----
        img (str):
            Path to the image file.
        txt (str):
            Path to the YOLO annotation text file.

    Returns:
    -------
        None

    """
    image = cv2.cvtColor(cv2.imread(img), cv2.COLOR_BGR2RGB)
    bndboxes: list[str] = Path(txt).read_text().splitlines()

    for bndbox in bndboxes:
        parts: list[str] = bndbox.split()
        label = int(parts[0])
        x_center = float(parts[1])
        y_center = float(parts[2])
        width = float(parts[3])
        height = float(parts[4])

        xmin, ymin, xmax, ymax = yolo_to_pascal_box(
            (x_center, y_center, width, height), (image.shape[1], image.shape[0])
        )

        _draw_annotation(image, label, (xmin, ymin, xmax, ymax))

    plt.figure(figsize=(10, 8))
    plt.imshow(image)
    plt.axis("off")
    plt.show()
