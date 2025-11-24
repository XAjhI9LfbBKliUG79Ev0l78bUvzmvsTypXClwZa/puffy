from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = Path(BASE_DIR, 'uploads')
UPLOAD_DIR.mkdir(exist_ok=True)
