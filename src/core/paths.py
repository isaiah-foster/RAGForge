from os import mkdir
from pathlib import Path
import platform

def get_app_dir() -> Path:
    system = platform.system()

    if system == "Darwin": #apple
        base = Path.home() / "Library" / "Application Support" / "ragforge"
    elif system == "Linux":
        base = Path.home() / ".config" / "ragforge"
    else:  # Windows
        base = Path.home() / "AppData" / "Roaming" / "ragforge"

    base.mkdir(parents=True, exist_ok=True)
    return base

APP_DIR = get_app_dir()
CONFIG_PATH = APP_DIR / "config.json"
DATA_BASE_PATH = APP_DIR / "db" / "chroma_db"
DATASET_PATH = APP_DIR / "db" / "datasets"

DATA_BASE_PATH.mkdir(parents=True, exist_ok=True)
DATASET_PATH.mkdir(parents=True, exist_ok=True)