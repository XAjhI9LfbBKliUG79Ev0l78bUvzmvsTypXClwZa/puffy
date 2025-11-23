import cv2
from .types import ImageArray

def to_grayscale(image: ImageArray) -> ImageArray:
    if len(image.shape) == 2:
        return image
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def gaussian_blur(image: ImageArray, kernel_size: int = 5) -> ImageArray:
    if kernel_size % 2 == 0:
        kernel_size += 1
    return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)

def adjust_brightness(image: ImageArray, value: int) -> ImageArray:
    return cv2.convertScaleAbs(image, alpha=1.0, beta=value)

def adjust_contrast(image: ImageArray, factor: float) -> ImageArray:
    return cv2.convertScaleAbs(image, alpha=factor, beta=0)

def detect_edges(image: ImageArray, threshold1: int = 100, threshold2: int = 200) -> ImageArray:
    return cv2.Canny(image, threshold1, threshold2)
