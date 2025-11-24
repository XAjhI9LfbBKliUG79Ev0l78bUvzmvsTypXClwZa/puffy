import numpy as np

from puffy.core.adjustments import adjust_brightness_contrast, adjust_color_balance
from puffy.core.effects import add_noise, blur
from puffy.core.transform import resize


def test_resize():
    # Create a dummy image
    image = np.zeros((100, 100, 3), dtype=np.uint8)

    # Resize the image
    resized_image = resize(image, 50, 50)

    # Check the dimensions of the resized image
    assert resized_image.shape == (50, 50, 3)

def test_adjust_brightness_contrast():
    # Create a dummy image
    image = np.zeros((100, 100, 3), dtype=np.uint8)

    # Adjust brightness and contrast
    adjusted_image = adjust_brightness_contrast(image, 10, 1.5)

    # Check the dimensions of the adjusted image
    assert adjusted_image.shape == (100, 100, 3)

def test_adjust_color_balance():
    # Create a dummy image
    image = np.zeros((100, 100, 3), dtype=np.uint8)

    # Adjust color balance
    adjusted_image = adjust_color_balance(image, 10, 0, -10)

    # Check the dimensions of the adjusted image
    assert adjusted_image.shape == (100, 100, 3)

def test_add_noise():
    # Create a dummy image
    image = np.zeros((100, 100, 3), dtype=np.uint8)

    # Add gaussian noise
    noisy_image = add_noise(image, "gaussian", 0.1)
    assert noisy_image.shape == (100, 100, 3)

    # Add salt & pepper noise
    noisy_image = add_noise(image, "salt_pepper", 0.1)
    assert noisy_image.shape == (100, 100, 3)


def test_blur():
    # Create a dummy image
    image = np.zeros((100, 100, 3), dtype=np.uint8)

    # Apply average blur
    blurred_image = blur(image, "average", 5)
    assert blurred_image.shape == (100, 100, 3)

    # Apply gaussian blur
    blurred_image = blur(image, "gaussian", 5)
    assert blurred_image.shape == (100, 100, 3)

    # Apply median blur
    blurred_image = blur(image, "median", 5)
    assert blurred_image.shape == (100, 100, 3)
