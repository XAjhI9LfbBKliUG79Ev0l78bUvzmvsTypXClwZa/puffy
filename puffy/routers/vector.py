from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse, FileResponse
import uuid
from puffy.core.vector.editor import VectorEditor
from puffy.config import UPLOAD_DIR

router = APIRouter()


@router.post("/vector/new", response_class=RedirectResponse)
async def new_vector_canvas(
    request: Request,
    width: int = Form(800),
    height: int = Form(600),
    units: str = Form("px"),
):
    svg_id = f"{uuid.uuid4()}.svg"
    save_path = UPLOAD_DIR / svg_id
    VectorEditor.create_canvas(
        filepath=save_path, width=width, height=height, units=units
    )
    return RedirectResponse(f"/vector?svg_id={svg_id}", status_code=303)


@router.post("/vector/add-shape")
async def add_shape(
    request: Request,
    svg_id: str = Form(...),
    shape: str = Form(...),
    x: float = Form(...),
    y: float = Form(...),
    width: float = Form(...),
    height: float = Form(...),
    fill: str = Form(...),
    stroke: str = Form(...),
    stroke_width: float = Form(...),
):
    filepath = UPLOAD_DIR / svg_id
    editor = VectorEditor(filepath)
    if shape == "rect":
        editor.add_rect(x, y, width, height, fill, stroke, stroke_width)
    editor.save()
    return {"status": "ok"}


@router.get("/vector/download/{svg_id}")
async def download_svg(svg_id: str):
    filepath = UPLOAD_DIR / svg_id
    return FileResponse(filepath, media_type="image/svg+xml", filename=svg_id)
