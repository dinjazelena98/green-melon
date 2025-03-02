"""Unit tests for the annot module that performs conversion between different bounding box formats (Pascal VOC to YOLO)."""  # noqa: E501

import pytest

from green_melon.annot import PascalBox, YoloBox, pascal_to_yolo_box, yolo_to_pascal_box


@pytest.mark.parametrize(
    ("size", "pascal_bbox", "expected_yolo_bbox"),
    [
        ((200, 100), PascalBox(50, 25, 150, 75), YoloBox(0.5, 0.5, 0.5, 0.5)),
        ((400, 200), PascalBox(100, 50, 300, 150), YoloBox(0.5, 0.5, 0.5, 0.5)),
        ((300, 300), PascalBox(30, 60, 180, 210), YoloBox(0.35, 0.45, 0.5, 0.5)),
    ],
)
def test_pascal_to_yolo_box(
    size: tuple[int, int], pascal_bbox: PascalBox, expected_yolo_bbox: YoloBox
) -> None:
    """
    Test conversion from a Pascal VOC bounding box to a YOLO bounding box for multiple input cases.

    Args:
    ----
        size (tuple[int, int]): The image dimensions in pixels (width, height).
        pascal_bbox (PascalBox): The input Pascal VOC bounding box.
        expected_yolo_bbox (YoloBox): The expected YOLO bounding box output.

    """
    result: YoloBox = pascal_to_yolo_box(size, pascal_bbox)
    assert result == expected_yolo_bbox
    assert isinstance(result, YoloBox)
    assert tuple(result) == tuple(expected_yolo_bbox)  # test __iter__ of dataclass
    assert vars(result) == vars(expected_yolo_bbox)


@pytest.mark.parametrize(
    ("size", "yolo_bbox", "expected_pascal_bbox"),
    [
        ((200, 100), YoloBox(0.5, 0.5, 0.5, 0.5), PascalBox(50, 25, 150, 75)),
        ((400, 200), YoloBox(0.5, 0.5, 0.5, 0.5), PascalBox(100, 50, 300, 150)),
        ((300, 300), YoloBox(0.35, 0.45, 0.5, 0.5), PascalBox(30, 60, 180, 210)),
    ],
)
def test_yolo_to_pascal(
    size: tuple[int, int], yolo_bbox: YoloBox, expected_pascal_bbox: PascalBox
) -> None:
    """
    Test conversion from a YOLO bounding box to a Pascal VOC bounding box for multiple input cases.

    Args:
    ----
        size (tuple[int, int]): The image dimensions in pixels (width, height).
        yolo_bbox (YoloBox): The input YOLO bounding box.
        expected_pascal_bbox (PascalBox): The expected Pascal VOC bounding box output.

    """
    result: PascalBox = yolo_to_pascal_box(size, yolo_bbox)
    assert result == expected_pascal_bbox
    assert isinstance(result, PascalBox)
    assert tuple(result) == tuple(expected_pascal_bbox)  # test __iter__ of dataclass
    assert vars(result) == vars(expected_pascal_bbox)
