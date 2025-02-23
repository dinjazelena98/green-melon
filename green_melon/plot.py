"""Utility functions for all sorts of stuff."""

import xml.etree.ElementTree as ET
from pathlib import Path

import cv2
import matplotlib.pyplot as plt

from green_melon.convert_annot import IDS_TO_LABELS


def _convert_to_absolute_coordinates(
    yolo_coordinates: tuple[float, float, float, float], image_size: tuple[int, int]
) -> tuple[int, int, int, int]:
    """
    Convert bounding box coordinates from YOLO format to absolute pixel coordinates.

    YOLO annotations use normalized values with the format (x_center, y_center, width, height),
    where the coordinates are relative to the image dimensions. This function converts these
    normalized values into absolute pixel coordinates given the image size.

    Args:
    ----
        yolo_coordinates (tuple[float, float, float, float]):
            A tuple (x_center, y_center, width, height) with normalized values.
        image_size (tuple[int, int]):
            A tuple (width, height) representing the dimensions of the image in pixels.

    Returns:
    -------
        tuple[int, int, int, int]:
            A tuple (x_min, y_min, x_max, y_max) representing the bounding box in absolute pixel coordinates.

    """  # noqa: E501
    x_center, y_center, box_width, box_height = yolo_coordinates
    img_width, img_height = image_size

    x_max: float = img_width * x_center + (box_width * img_width / 2)
    x_min: float = img_width * x_center - (box_width * img_width / 2)
    y_max: float = img_height * y_center + (box_height * img_height / 2)
    y_min: float = img_height * y_center - (box_height * img_height / 2)

    return int(x_min), int(y_min), int(x_max), int(y_max)


def plot_pascal_voc_img(img: str, xml: str) -> None:
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

        cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (255, 0, 0), 5)
        cv2.putText(
            image,
            obj.find("name").text.strip(),
            (xmin, max(ymin - 10, 0)),
            cv2.FONT_HERSHEY_SIMPLEX,
            2,
            (255, 0, 0),
            3,
        )
    plt.figure(figsize=(10, 8))
    plt.imshow(image)
    plt.axis("off")
    plt.show()


def plot_yolo_txt_img(img: str, txt: str) -> None:
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

        xmin, ymin, xmax, ymax = _convert_to_absolute_coordinates(
            (x_center, y_center, width, height), (image.shape[1], image.shape[0])
        )

        cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (255, 0, 0), 5)
        cv2.putText(
            image,
            IDS_TO_LABELS[label],
            (xmin, max(ymin - 10, 0)),
            cv2.FONT_HERSHEY_SIMPLEX,
            2,
            (255, 0, 0),
            3,
        )
    plt.figure(figsize=(10, 8))
    plt.imshow(image)
    plt.axis("off")
    plt.show()
