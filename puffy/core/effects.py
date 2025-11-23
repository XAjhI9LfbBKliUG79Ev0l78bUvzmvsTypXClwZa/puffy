import numpy as np
import cv2
from .types import ImageArray

def add_noise(image: ImageArray, noise_type: str = "gaussian", intensity: float = 0.1) -> ImageArray:
    """Adds noise to an image."""
    h, w, c = image.shape
    if noise_type == "gaussian":
        mean = 0
        var = intensity * 255
        sigma = var ** 0.5
        gauss = np.random.normal(mean, sigma, (h, w, c))
        noisy = np.clip(image + gauss, 0, 255)
        return ImageArray(noisy.astype(np.uint8))
    elif noise_type == "salt_pepper":
        noisy = np.copy(image)
        # Salt
        num_salt = np.ceil(intensity * image.size * 0.5)
        coords = [np.random.randint(0, i, int(num_salt)) for i in image.shape]
        noisy[coords[0], coords[1], :] = 255
        # Pepper
        num_pepper = np.ceil(intensity * image.size * 0.5)
        coords = [np.random.randint(0, i, int(num_pepper)) for i in image.shape]
        noisy[coords[0], coords[1], :] = 0
        return ImageArray(noisy)
    return image

def blur(image: ImageArray, blur_type: str = "gaussian", kernel_size: int = 5) -> ImageArray:
    """Applies a blur to an image."""
    # Kernel size must be odd
    if kernel_size % 2 == 0:
        kernel_size += 1

    if blur_type == "average":
        return ImageArray(cv2.blur(image, (kernel_size, kernel_size)))
    elif blur_type == "gaussian":
        return ImageArray(cv2.GaussianBlur(image, (kernel_size, kernel_size), 0))
    elif blur_type == "median":
        return ImageArray(cv2.medianBlur(image, kernel_size))
    return image
