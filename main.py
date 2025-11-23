from fastapi import FastAPI, Request, Form, UploadFile, File, Depends, BackgroundTasks
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import shutil
import uuid
import os
from puffy.core.editor import ImageEditor
from puffy.dependencies import ImageFileHandler
from typing import Optional, List

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = Path(BASE_DIR, 'uploads')
UPLOAD_DIR.mkdir(exist_ok=True)

app.mount("/static", StaticFiles(directory=UPLOAD_DIR), name="static")

templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'puffy/templates')))

def cleanup_file(path: Path):
    if path.exists():
        os.remove(path)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload", response_class=HTMLResponse)
async def upload_file(request: Request, file: UploadFile = File(...)):
    allowed_extensions = {".jpg", ".jpeg", ".png", ".gif", ".tiff"}
    ext = Path(file.filename).suffix.lower()
    if ext not in allowed_extensions:
        return templates.TemplateResponse("error.html", {"request": request, "message": "Unsupported file format."})

    image_id = f"{uuid.uuid4()}{ext}"
    save_path = UPLOAD_DIR / image_id

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return templates.TemplateResponse("editor.html", {"request": request, "image_id": image_id, "alt_text": "uploaded image"})

@app.post("/resize", response_class=HTMLResponse)
async def resize_image(
    request: Request,
    width: int = Form(..., gt=0),
    height: int = Form(..., gt=0),
    interpolation: str = Form("bicubic"),
    handler: ImageFileHandler = Depends(ImageFileHandler)
):
    new_path = handler.get_new_path()
    editor = ImageEditor.open(handler.original_path)
    editor.resize(width, height, interpolation=interpolation)
    editor.save(new_path)
    handler.cleanup()
    context = {
        "request": request,
        "image_id": new_path.name,
        "alt_text": f"resized image ({width}x{height})",
        "width": width,
        "height": height,
        "interpolation": interpolation,
    }
    return templates.TemplateResponse("editor.html", context)

@app.post("/crop", response_class=HTMLResponse)
async def crop_image(
    request: Request,
    x: int = Form(..., ge=0),
    y: int = Form(..., ge=0),
    width: int = Form(..., gt=0),
    height: int = Form(..., gt=0),
    handler: ImageFileHandler = Depends(ImageFileHandler)
):
    new_path = handler.get_new_path()
    try:
        editor = ImageEditor.open(handler.original_path)
        editor.crop(x, y, width, height)
        editor.save(new_path)
        handler.cleanup()
        context = {
            "request": request,
            "image_id": new_path.name,
            "alt_text": f"cropped image ({width}x{height} at {x},{y})",
            "x": x,
            "y": y,
            "crop_width": width,
            "crop_height": height,
        }
        return templates.TemplateResponse("editor.html", context)
    except ValueError as e:
        return templates.TemplateResponse("error.html", {"request": request, "message": str(e)})

@app.post("/flip", response_class=HTMLResponse)
async def flip_image(
    request: Request,
    direction: List[str] = Form(default=[]),
    handler: ImageFileHandler = Depends(ImageFileHandler)
):
    if not direction:
        return templates.TemplateResponse("editor.html", {"request": request, "image_id": handler.image_id, "alt_text": "flipped none", "direction": []})

    new_path = handler.get_new_path()
    horizontal = "horizontal" in direction
    vertical = "vertical" in direction

    editor = ImageEditor.open(handler.original_path)
    editor.flip(horizontal=horizontal, vertical=vertical)
    editor.save(new_path)
    handler.cleanup()
    context = {
        "request": request,
        "image_id": new_path.name,
        "alt_text": f"flipped {', '.join(direction) if direction else 'none'}",
        "direction": direction,
    }
    return templates.TemplateResponse("editor.html", context)

@app.post("/rotate", response_class=HTMLResponse)
async def rotate_image(
    request: Request,
    angle: float = Form(...),
    center_x: Optional[int] = Form(None),
    center_y: Optional[int] = Form(None),
    handler: ImageFileHandler = Depends(ImageFileHandler)
):
    new_path = handler.get_new_path()
    center = (center_x, center_y) if center_x is not None and center_y is not None else None
    editor = ImageEditor.open(handler.original_path)
    editor.rotate(angle, center=center)
    editor.save(new_path)
    handler.cleanup()
    context = {
        "request": request,
        "image_id": new_path.name,
        "alt_text": f"rotated image ({angle} degrees)",
        "angle": angle,
        "center_x": center_x,
        "center_y": center_y,
    }
    return templates.TemplateResponse("editor.html", context)

@app.post("/adjust-brightness-contrast", response_class=HTMLResponse)
async def adjust_brightness_contrast(
    request: Request,
    brightness: int = Form(0),
    contrast: float = Form(1.0),
    handler: ImageFileHandler = Depends(ImageFileHandler)
):
    new_path = handler.get_new_path()
    editor = ImageEditor.open(handler.original_path)
    editor.adjust_brightness_contrast(brightness=brightness, contrast=contrast)
    editor.save(new_path)
    handler.cleanup()
    context = {
        "request": request,
        "image_id": new_path.name,
        "alt_text": "brightness/contrast adjusted",
        "brightness": brightness,
        "contrast": contrast,
    }
    return templates.TemplateResponse("editor.html", context)

@app.post("/adjust-color-balance", response_class=HTMLResponse)
async def adjust_color_balance(
    request: Request,
    red: int = Form(0),
    green: int = Form(0),
    blue: int = Form(0),
    handler: ImageFileHandler = Depends(ImageFileHandler)
):
    new_path = handler.get_new_path()
    editor = ImageEditor.open(handler.original_path)
    editor.adjust_color_balance(red=red, green=green, blue=blue)
    editor.save(new_path)
    handler.cleanup()
    context = {
        "request": request,
        "image_id": new_path.name,
        "alt_text": "color balance adjusted",
        "red": red,
        "green": green,
        "blue": blue,
    }
    return templates.TemplateResponse("editor.html", context)

@app.post("/add-noise", response_class=HTMLResponse)
async def add_noise(
    request: Request,
    noise_type: str = Form("gaussian"),
    intensity: float = Form(0.1),
    handler: ImageFileHandler = Depends(ImageFileHandler)
):
    new_path = handler.get_new_path()
    editor = ImageEditor.open(handler.original_path)
    editor.add_noise(noise_type=noise_type, intensity=intensity)
    editor.save(new_path)
    handler.cleanup()
    context = {
        "request": request,
        "image_id": new_path.name,
        "alt_text": f"{noise_type} noise added",
        "noise_type": noise_type,
        "intensity": intensity,
    }
    return templates.TemplateResponse("editor.html", context)

@app.post("/blur", response_class=HTMLResponse)
async def blur(
    request: Request,
    blur_type: str = Form("gaussian"),
    kernel_size: int = Form(5, gt=0),
    handler: ImageFileHandler = Depends(ImageFileHandler)
):
    new_path = handler.get_new_path()
    editor = ImageEditor.open(handler.original_path)
    editor.blur(blur_type=blur_type, kernel_size=kernel_size)
    editor.save(new_path)
    handler.cleanup()
    context = {
        "request": request,
        "image_id": new_path.name,
        "alt_text": f"{blur_type} blur applied",
        "blur_type": blur_type,
        "kernel_size": kernel_size,
    }
    return templates.TemplateResponse("editor.html", context)

@app.post("/download")
async def download_image(
    background_tasks: BackgroundTasks,
    image_id: str = Form(...),
    format: str = Form("jpeg"),
    quality: int = Form(95),
    handler: ImageFileHandler = Depends(ImageFileHandler)
):
    ext = f".{format.lower()}"
    # Create a temporary path for the download
    download_id = f"{uuid.uuid4()}{ext}"
    download_path = UPLOAD_DIR / download_id

    editor = ImageEditor.open(handler.original_path)
    editor.save(download_path, quality=quality)

    # Schedule the cleanup of the temporary file
    background_tasks.add_task(cleanup_file, download_path)

    return FileResponse(download_path, media_type=f"image/{format}", filename=f"edited_image{ext}")
