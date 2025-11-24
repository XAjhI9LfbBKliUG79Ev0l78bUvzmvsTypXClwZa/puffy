from pathlib import Path
from typing import Callable, Any

from .dependencies import ImageFileHandler


def process_image_and_save(
    handler: ImageFileHandler,
    operation: Callable[..., Any],
    **kwargs,
) -> Path:
    """
    Applies an operation to an image, saves the result, and cleans up.

    Args:
        handler: The ImageFileHandler dependency with an initialized ImageEditor.
        operation: A method from the ImageEditor class (e.g., editor.resize).
        **kwargs: The arguments for the operation method.

    Returns:
        The path of the new image file.
    """
    new_path = handler.get_new_path()
    operation(handler.editor, **kwargs)
    handler.editor.save(new_path)
    handler.cleanup()
    return new_path
