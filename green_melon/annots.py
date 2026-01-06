"""Module for conversion of bounding box formats."""

from __future__ import annotations

from pydantic import BaseModel


class PascalBbox(BaseModel):
    """Pascal VOC bounding box format: (xmin, ymin, xmax, ymax) in absolute pixels."""

    xmin: int
    ymin: int
    xmax: int
    ymax: int

    def to_yolo(self, image_width: int, image_height: int, class_id: int) -> YoloBbox:
        """Convert Pascal VOC bounding box to YOLO format."""
        assert image_width > 0
        assert image_height > 0
        assert 0 <= self.xmin < self.xmax <= image_width
        assert 0 <= self.ymin < self.ymax <= image_height

        # corners
        bbox_width: float = self.xmax - self.xmin
        bbox_height: float = self.ymax - self.ymin

        # center
        x_center: float = self.xmin + bbox_width / 2
        y_center: float = self.ymin + bbox_height / 2

        # normalize
        x_center /= image_width
        y_center /= image_height
        bbox_width /= image_width
        bbox_height /= image_height

        return YoloBbox(
            class_id=class_id,
            x_center=x_center,
            y_center=y_center,
            width=bbox_width,
            height=bbox_height,
        )


class YoloBbox(BaseModel):
    """YOLO bounding box format: (x_center, y_center, width, height) in normalized coordinates."""

    class_id: int
    x_center: float
    y_center: float
    width: float
    height: float

    def to_yolo_lines(self, precision: int = 6) -> str:
        """Convert to YOLO format string with specified precision."""
        return (
            f"{self.class_id}"
            f"{self.x_center:.{precision}f}"
            f"{self.y_center:.{precision}f}"
            f"{self.width:.{precision}f}"
            f"{self.height:.{precision}f}"
        )
