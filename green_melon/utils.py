"""Utility functions for all sorts of stuff."""

import xml.etree.ElementTree as ET

import cv2
import matplotlib.pyplot as plt


def plot_pascal_voc_img(img: str, xml: str) -> None:
    """
    Plot image with bounding boxes annotated with Pascal VOC format.

    Args:
        img: str -> Path to image.
        xml: str -> Path to annot.

    Returns:
        None

    """
    tree = ET.parse(xml)  # noqa: S314
    root = tree.getroot()

    image = cv2.cvtColor(cv2.imread(img), cv2.COLOR_BGR2RGB)

    for obj in root.findall("object"):
        bndbox = obj.find("bndbox")  # type: ignore[union-attr]

        xmin = int(bndbox.find("xmin").text)  # type: ignore[union-attr, arg-type]
        ymin = int(bndbox.find("ymin").text)  # type: ignore[union-attr, arg-type]
        xmax = int(bndbox.find("xmax").text)  # type: ignore[union-attr, arg-type]
        ymax = int(bndbox.find("ymax").text)  # type: ignore[union-attr, arg-type]

        cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (255, 0, 0), 5)
        cv2.putText(
            image,
            obj.find("name").text.strip(),  # type: ignore[union-attr]
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
