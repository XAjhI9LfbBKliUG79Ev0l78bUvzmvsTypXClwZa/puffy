from pathlib import Path
import cv2
from .types import ImageArray


def load_image(path: str | Path) -> ImageArray:
    """Loads an image from the specified path."""
    image = cv2.imread(str(path))
    if image is None:
        raise FileNotFoundError(f"Image not found at {path}")
    return ImageArray(image)


def save_image(image: ImageArray, path: str | Path, quality: int = 95) -> None:
    """Saves an image to the specified path with optional quality settings for JPEG."""
    ext = Path(path).suffix.lower()
    if ext in [".jpg", ".jpeg"]:
        params = [cv2.IMWRITE_JPEG_QUALITY, quality]
        if not cv2.imwrite(str(path), image, params):
            raise IOError(f"Could not save JPEG image to {path}")
    else:
        if not cv2.imwrite(str(path), image):
            raise IOError(f"Could not save image to {path}")
