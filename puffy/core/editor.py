from __future__ import annotations

import copy
from dataclasses import dataclass, field
from pathlib import Path

from . import adjustments, effects, io, transform
from .types import ImageArray


@dataclass
class ImageEditor:
    _image: ImageArray | None = field(default=None, repr=False)

    @property
    def image(self) -> ImageArray:
        if self._image is None:
            raise ValueError("No image loaded")
        return self._image

    @classmethod
    def open(cls, path: str | Path) -> ImageEditor:
        return cls(_image=io.load_image(path))

    def save(self, path: str | Path, quality: int = 95) -> ImageEditor:
        io.save_image(self.image, path, quality=quality)
        return self

    def resize(
        self, width: int, height: int, interpolation: str = "bicubic"
    ) -> ImageEditor:
        self._image = transform.resize(self.image, width, height, interpolation)
        return self

    def rotate(
        self, angle: float, center: tuple[int, int] | None = None
    ) -> ImageEditor:
        self._image = transform.rotate(self.image, angle, center)
        return self

    def crop(self, x: int, y: int, width: int, height: int) -> ImageEditor:
        self._image = transform.crop(self.image, x, y, width, height)
        return self

    def flip(self, horizontal: bool = True, vertical: bool = False) -> ImageEditor:
        self._image = transform.flip(self.image, horizontal, vertical)
        return self

    def adjust_brightness_contrast(
        self, brightness: int = 0, contrast: float = 1.0
    ) -> ImageEditor:
        self._image = adjustments.adjust_brightness_contrast(
            self.image, brightness, contrast
        )
        return self

    def adjust_color_balance(
        self, red: int = 0, green: int = 0, blue: int = 0
    ) -> ImageEditor:
        self._image = adjustments.adjust_color_balance(self.image, red, green, blue)
        return self

    def add_noise(
        self, noise_type: str = "gaussian", intensity: float = 0.1
    ) -> ImageEditor:
        self._image = effects.add_noise(self.image, noise_type, intensity)
        return self

    def blur(self, blur_type: str = "gaussian", kernel_size: int = 5) -> ImageEditor:
        self._image = effects.blur(self.image, blur_type, kernel_size)
        return self

    def clone(self) -> ImageEditor:
        return ImageEditor(_image=copy.deepcopy(self._image))
