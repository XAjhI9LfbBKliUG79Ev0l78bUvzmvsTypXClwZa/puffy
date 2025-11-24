from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from typing import Optional

router = APIRouter()
templates = Jinja2Templates(
    directory=str(Path(__file__).resolve().parent.parent / "templates")
)


@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/vector", response_class=HTMLResponse)
async def vector_editor(request: Request, svg_id: Optional[str] = None):
    return templates.TemplateResponse(
        "vector_editor.html", {"request": request, "svg_id": svg_id}
    )
