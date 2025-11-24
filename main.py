from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from puffy.routers import ui, vector, image
from puffy.config import UPLOAD_DIR, BASE_DIR

app = FastAPI()

app.mount("/static", StaticFiles(directory=UPLOAD_DIR), name="static")
app.mount(
    "/js", StaticFiles(directory=str(Path(BASE_DIR, "puffy/static/js"))), name="js"
)

app.include_router(ui.router)
app.include_router(vector.router)
app.include_router(image.router)
