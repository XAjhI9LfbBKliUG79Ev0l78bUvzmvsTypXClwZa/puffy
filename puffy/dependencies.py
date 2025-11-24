import os
import uuid
from pathlib import Path

from fastapi import Form, HTTPException

from .core.editor import ImageEditor

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = Path(BASE_DIR, "uploads")


def is_safe_path(basedir, path, follow_symlinks=True):
    if follow_symlinks:
        return os.path.realpath(path).startswith(str(basedir))
    return os.path.abspath(path).startswith(str(basedir))


class ImageFileHandler:
    def __init__(self, image_id: str = Form(...)):
        self.image_id = image_id
        self.original_path = UPLOAD_DIR / self.image_id
        if (
            not is_safe_path(UPLOAD_DIR, self.original_path)
            or not self.original_path.is_file()
        ):
            raise HTTPException(status_code=404, detail="Image not found.")

        self.editor = ImageEditor.open(self.original_path)

    def get_new_path(self) -> Path:
        ext = self.original_path.suffix
        new_image_id = f"{uuid.uuid4()}{ext}"
        return UPLOAD_DIR / new_image_id

    def cleanup(self):
        if self.original_path.exists():
            os.remove(self.original_path)
