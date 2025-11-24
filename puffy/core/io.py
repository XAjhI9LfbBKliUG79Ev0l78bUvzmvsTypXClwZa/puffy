from pathlib import Path

import cv2
import numpy as np

from .types import ImageArray


def load_image(path: str | Path) -> ImageArray:
    """Loads an image from the specified path."""
    image = cv2.imread(str(path))
    if image is None:
        raise FileNotFoundError(f"Image not found at {path}")
    return image.astype(np.uint8)


def save_image(image: ImageArray, path: str | Path, quality: int = 95) -> None:
    """Saves an image to the specified path."""
    ext = Path(path).suffix.lower()
    if ext == ".jpeg" or ext == ".jpg":
        params = [cv2.IMWRITE_JPEG_QUALITY, quality]
        if not cv2.imwrite(str(path), image, params):
            raise OSError(f"Could not save JPEG image to {path}")
    else:
        if not cv2.imwrite(str(path), image):
            raise OSError(f"Could not save image to {path}")
