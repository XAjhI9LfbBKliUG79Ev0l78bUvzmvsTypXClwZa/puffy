from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(
    directory=str(Path(__file__).resolve().parent.parent / "templates")
)


@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(request, "index.html")


@router.get("/vector", response_class=HTMLResponse)
async def vector_editor(request: Request, svg_id: str | None = None):
    return templates.TemplateResponse(
        request, "vector_editor.html", {"svg_id": svg_id}
    )
