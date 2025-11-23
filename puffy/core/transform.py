import cv2
import numpy as np
from .types import ImageArray
from typing import Optional

def resize(image: ImageArray, width: int, height: int, interpolation: str = "bicubic") -> ImageArray:
    """Resizes an image with a specified interpolation method."""
    inter_map = {
        "nearest": cv2.INTER_NEAREST,
        "bilinear": cv2.INTER_LINEAR,
        "bicubic": cv2.INTER_CUBIC,
    }
    interpolation_flag = inter_map.get(interpolation, cv2.INTER_CUBIC)
    return ImageArray(cv2.resize(image, (width, height), interpolation=interpolation_flag))

def crop(image: ImageArray, x: int, y: int, width: int, height: int) -> ImageArray:
    """Crops an image to a specified rectangle."""
    if x < 0 or y < 0 or x + width > image.shape[1] or y + height > image.shape[0]:
        raise ValueError("Crop coordinates are out of bounds")
    return ImageArray(image[y:y+height, x:x+width])

def flip(image: ImageArray, horizontal: bool = True, vertical: bool = False) -> ImageArray:
    """Flips an image horizontally, vertically, or both."""
    if horizontal and vertical:
        flip_code = -1
    elif horizontal:
        flip_code = 1
    elif vertical:
        flip_code = 0
    else:
        return image
    return ImageArray(cv2.flip(image, flip_code))

def rotate(image: ImageArray, angle: float, center: Optional[tuple[int, int]] = None) -> ImageArray:
    """Rotates an image by a specified angle and center."""
    (h, w) = image.shape[:2]
    if center is None:
        center = (w // 2, h // 2)

    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    return ImageArray(cv2.warpAffine(image, M, (w, h)))
