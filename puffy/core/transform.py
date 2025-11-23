import cv2
from .types import ImageArray

def resize(image: ImageArray, width: int, height: int) -> ImageArray:
    return cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)

def rotate(image: ImageArray, angle: float) -> ImageArray:
    h, w = image.shape[:2]
    center = (w // 2, h // 2)
    matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(image, matrix, (w, h))

def crop(image: ImageArray, x: int, y: int, width: int, height: int) -> ImageArray:
    return image[y:y+height, x:x+width]

def flip(image: ImageArray, horizontal: bool = True) -> ImageArray:
    flip_code = 1 if horizontal else 0
    return cv2.flip(image, flip_code)
