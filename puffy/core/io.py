import cv2
from pathlib import Path
from .types import ImageArray

def load_image(path: str | Path) -> ImageArray:
    image = cv2.imread(str(path))
    if image is None:
        raise FileNotFoundError(f"Could not load image from {path}")
    return image

def save_image(image: ImageArray, path: str | Path) -> None:
    cv2.imwrite(str(path), image)
