from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
import copy

from .types import ImageArray
from . import io, transform, filters

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

    def save(self, path: str | Path) -> ImageEditor:
        io.save_image(self.image, path)
        return self

    def resize(self, width: int, height: int) -> ImageEditor:
        self._image = transform.resize(self.image, width, height)
        return self

    def rotate(self, angle: float) -> ImageEditor:
        self._image = transform.rotate(self.image, angle)
        return self

    def crop(self, x: int, y: int, width: int, height: int) -> ImageEditor:
        self._image = transform.crop(self.image, x, y, width, height)
        return self

    def flip(self, horizontal: bool = True) -> ImageEditor:
        self._image = transform.flip(self.image, horizontal)
        return self

    def grayscale(self) -> ImageEditor:
        self._image = filters.to_grayscale(self.image)
        return self

    def blur(self, kernel_size: int = 5) -> ImageEditor:
        self._image = filters.gaussian_blur(self.image, kernel_size)
        return self

    def brightness(self, value: int) -> ImageEditor:
        self._image = filters.adjust_brightness(self.image, value)
        return self

    def contrast(self, factor: float) -> ImageEditor:
        self._image = filters.adjust_contrast(self.image, factor)
        return self

    def edges(self) -> ImageEditor:
        self._image = filters.detect_edges(self.image)
        return self

    def clone(self) -> ImageEditor:
        return ImageEditor(_image=copy.deepcopy(self._image))
