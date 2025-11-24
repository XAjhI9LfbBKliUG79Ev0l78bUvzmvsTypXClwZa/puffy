import os
import shutil
import uuid
from pathlib import Path
from typing import List

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    File,
    Form,
    Request,
    UploadFile,
)
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates

from puffy.config import UPLOAD_DIR
from puffy.core.editor import ImageEditor
from puffy.dependencies import ImageFileHandler
from puffy.handlers import process_image_and_save

router = APIRouter()
templates = Jinja2Templates(
    directory=str(Path(__file__).resolve().parent.parent / "templates")
)


def cleanup_file(path: Path):
    if path.exists():
        os.remove(path)


@router.post("/upload", response_class=HTMLResponse)
async def upload_file(request: Request, file: UploadFile = File(...)):
    if file.filename is None:
        return templates.TemplateResponse(
            request, "error.html", {"message": "Invalid file upload."}
        )
    allowed_extensions = {".jpg", ".jpeg", ".png", ".gif", ".tiff"}
    ext = Path(file.filename).suffix.lower()
    if ext not in allowed_extensions:
        return templates.TemplateResponse(
            request, "error.html", {"message": "Unsupported file format."}
        )

    image_id = f"{uuid.uuid4()}{ext}"
    save_path = UPLOAD_DIR / image_id

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return templates.TemplateResponse(
        request,
        "editor.html",
        {"image_id": image_id, "alt_text": "uploaded image"},
    )


@router.post("/resize", response_class=HTMLResponse)
async def resize_image(
    request: Request,
    width: int = Form(..., gt=0),
    height: int = Form(..., gt=0),
    interpolation: str = Form("bicubic"),
    handler: ImageFileHandler = Depends(ImageFileHandler),
):
    new_path = process_image_and_save(
        handler,
        ImageEditor.resize,
        width=width,
        height=height,
        interpolation=interpolation,
    )
    context = {
        "image_id": new_path.name,
        "alt_text": f"resized image ({width}x{height})",
        "width": width,
        "height": height,
        "interpolation": interpolation,
    }
    return templates.TemplateResponse(request, "editor.html", context)


@router.post("/crop", response_class=HTMLResponse)
async def crop_image(
    request: Request,
    x: int = Form(..., ge=0),
    y: int = Form(..., ge=0),
    width: int = Form(..., gt=0),
    height: int = Form(..., gt=0),
    handler: ImageFileHandler = Depends(ImageFileHandler),
):
    try:
        new_path = process_image_and_save(
            handler,
            ImageEditor.crop,
            x=x,
            y=y,
            width=width,
            height=height,
        )
        context = {
            "image_id": new_path.name,
            "alt_text": f"cropped image ({width}x{height} at {x},{y})",
            "x": x,
            "y": y,
            "crop_width": width,
            "crop_height": height,
        }
        return templates.TemplateResponse(request, "editor.html", context)
    except ValueError as e:
        return templates.TemplateResponse(
            request, "error.html", {"message": str(e)}
        )


@router.post("/flip", response_class=HTMLResponse)
async def flip_image(
    request: Request,
    direction: list[str] = Form(default=[]),
    handler: ImageFileHandler = Depends(ImageFileHandler),
):
    if not direction:
        return templates.TemplateResponse(
            request,
            "editor.html",
            {
                "image_id": handler.image_id,
                "alt_text": "flipped none",
                "direction": [],
            },
        )

    horizontal = "horizontal" in direction
    vertical = "vertical" in direction
    new_path = process_image_and_save(
        handler,
        ImageEditor.flip,
        horizontal=horizontal,
        vertical=vertical,
    )
    context = {
        "image_id": new_path.name,
        "alt_text": f"flipped {', '.join(direction) if direction else 'none'}",
        "direction": direction,
    }
    return templates.TemplateResponse(request, "editor.html", context)


@router.post("/rotate", response_class=HTMLResponse)
async def rotate_image(
    request: Request,
    angle: float = Form(...),
    center_x: int | None = Form(None),
    center_y: int | None = Form(None),
    handler: ImageFileHandler = Depends(ImageFileHandler),
):
    center = (
        (center_x, center_y) if center_x is not None and center_y is not None else None
    )
    new_path = process_image_and_save(
        handler,
        ImageEditor.rotate,
        angle=angle,
        center=center,
    )
    context = {
        "image_id": new_path.name,
        "alt_text": f"rotated image ({angle} degrees)",
        "angle": angle,
        "center_x": center_x,
        "center_y": center_y,
    }
    return templates.TemplateResponse(request, "editor.html", context)


@router.post("/adjust-brightness-contrast", response_class=HTMLResponse)
async def adjust_brightness_contrast(
    request: Request,
    brightness: int = Form(0),
    contrast: float = Form(1.0),
    handler: ImageFileHandler = Depends(ImageFileHandler),
):
    new_path = process_image_and_save(
        handler,
        ImageEditor.adjust_brightness_contrast,
        brightness=brightness,
        contrast=contrast,
    )
    context = {
        "image_id": new_path.name,
        "alt_text": "brightness/contrast adjusted",
        "brightness": brightness,
        "contrast": contrast,
    }
    return templates.TemplateResponse(request, "editor.html", context)


@router.post("/adjust-color-balance", response_class=HTMLResponse)
async def adjust_color_balance(
    request: Request,
    red: int = Form(0),
    green: int = Form(0),
    blue: int = Form(0),
    handler: ImageFileHandler = Depends(ImageFileHandler),
):
    new_path = process_image_and_save(
        handler,
        ImageEditor.adjust_color_balance,
        red=red,
        green=green,
        blue=blue,
    )
    context = {
        "image_id": new_path.name,
        "alt_text": "color balance adjusted",
        "red": red,
        "green": green,
        "blue": blue,
    }
    return templates.TemplateResponse(request, "editor.html", context)


@router.post("/add-noise", response_class=HTMLResponse)
async def add_noise(
    request: Request,
    noise_type: str = Form("gaussian"),
    intensity: float = Form(0.1),
    handler: ImageFileHandler = Depends(ImageFileHandler),
):
    new_path = process_image_and_save(
        handler,
        ImageEditor.add_noise,
        noise_type=noise_type,
        intensity=intensity,
    )
    context = {
        "image_id": new_path.name,
        "alt_text": f"{noise_type} noise added",
        "noise_type": noise_type,
        "intensity": intensity,
    }
    return templates.TemplateResponse(request, "editor.html", context)


@router.post("/blur", response_class=HTMLResponse)
async def blur(
    request: Request,
    blur_type: str = Form("gaussian"),
    kernel_size: int = Form(5, gt=0),
    handler: ImageFileHandler = Depends(ImageFileHandler),
):
    new_path = process_image_and_save(
        handler,
        ImageEditor.blur,
        blur_type=blur_type,
        kernel_size=kernel_size,
    )
    context = {
        "image_id": new_path.name,
        "alt_text": f"{blur_type} blur applied",
        "blur_type": blur_type,
        "kernel_size": kernel_size,
    }
    return templates.TemplateResponse(request, "editor.html", context)


@router.post("/download")
async def download_image(
    background_tasks: BackgroundTasks,
    image_id: str = Form(...),
    format: str = Form("jpeg"),
    quality: int = Form(95),
    handler: ImageFileHandler = Depends(ImageFileHandler),
):
    ext = f".{format.lower()}"
    download_id = f"{uuid.uuid4()}{ext}"
    download_path = UPLOAD_DIR / download_id

    editor = ImageEditor.open(handler.original_path)
    editor.save(download_path, quality=quality)

    background_tasks.add_task(cleanup_file, download_path)

    return FileResponse(
        download_path, media_type=f"image/{format}", filename=f"edited_image{ext}"
    )
