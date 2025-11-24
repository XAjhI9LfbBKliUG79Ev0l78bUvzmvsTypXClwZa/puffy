import os

import cv2
import numpy as np

# Create a dummy image
image = np.zeros((100, 100, 3), dtype=np.uint8)
image[:, :] = (0, 0, 255)  # Red color in BGR

# Create the assets directory if it doesn't exist
assets_dir = 'tests/assets'
if not os.path.exists(assets_dir):
    os.makedirs(assets_dir)

# Save the image
cv2.imwrite(os.path.join(assets_dir, 'test.png'), image)
