import numpy as np
import cv2
from .types import ImageArray


def adjust_brightness_contrast(
    image: ImageArray, brightness: int = 0, contrast: float = 1.0
) -> ImageArray:
    """Adjusts the brightness and contrast of an image."""
    # The formula is new_image = alpha * original_image + beta
    # alpha (contrast) and beta (brightness)
    adjusted = cv2.convertScaleAbs(image, alpha=contrast, beta=brightness)
    return ImageArray(adjusted)


def adjust_color_balance(
    image: ImageArray, red: int = 0, green: int = 0, blue: int = 0
) -> ImageArray:
    """Adjusts the color balance of an image."""
    b, g, r = cv2.split(image)

    # Add the value and clip to the 0-255 range
    b = np.clip(b.astype(np.int16) + blue, 0, 255).astype(np.uint8)
    g = np.clip(g.astype(np.int16) + green, 0, 255).astype(np.uint8)
    r = np.clip(r.astype(np.int16) + red, 0, 255).astype(np.uint8)

    return ImageArray(cv2.merge([b, g, r]))
