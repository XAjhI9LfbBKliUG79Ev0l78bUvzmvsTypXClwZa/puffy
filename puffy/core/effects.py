import cv2
import numpy as np

from .types import ImageArray


def add_noise(
    image: ImageArray, noise_type: str = "gaussian", intensity: float = 0.1
) -> ImageArray:
    """Adds noise to an image."""
    h, w, c = image.shape
    if noise_type == "gaussian":
        mean = 0
        var = intensity * 255
        sigma = var**0.5
        gauss = np.random.normal(mean, sigma, (h, w, c))
        noisy = np.clip(image + gauss, 0, 255)
        return noisy.astype(np.uint8)
    elif noise_type == "salt_pepper":
        noisy = np.copy(image)
        # Salt
        num_salt = np.ceil(intensity * image.size * 0.5)
        coords = [
            np.random.randint(0, i, int(num_salt)) for i in image.shape
        ]
        noisy[coords[0], coords[1], :] = 255
        # Pepper
        num_pepper = np.ceil(intensity * image.size * 0.5)
        coords = [
            np.random.randint(0, i, int(num_pepper)) for i in image.shape
        ]
        noisy[coords[0], coords[1], :] = 0
        return noisy.astype(np.uint8)
    return image


def blur(
    image: ImageArray, blur_type: str = "gaussian", kernel_size: int = 5
) -> ImageArray:
    """Applies a blur to an image."""
    # Kernel size must be odd
    if kernel_size % 2 == 0:
        kernel_size += 1

    if blur_type == "average":
        return cv2.blur(image, (kernel_size, kernel_size)).astype(np.uint8)
    elif blur_type == "gaussian":
        return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0).astype(
            np.uint8
        )
    elif blur_type == "median":
        return cv2.medianBlur(image, kernel_size).astype(np.uint8)
    return image
