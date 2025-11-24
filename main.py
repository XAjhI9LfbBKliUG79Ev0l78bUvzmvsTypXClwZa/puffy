from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from puffy.config import BASE_DIR, UPLOAD_DIR
from puffy.routers import image, ui, vector

app = FastAPI()

app.mount("/static", StaticFiles(directory=UPLOAD_DIR), name="static")
app.mount(
    "/js", StaticFiles(directory=str(Path(BASE_DIR, "puffy/static/js"))), name="js"
)

app.include_router(ui.router)
app.include_router(vector.router)
app.include_router(image.router)
