from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = REPO_ROOT / "src" / "core" / "config.json"
DATA_BASE_PATH = REPO_ROOT / "src" / "db" / "chroma_db"
DATASET_PATH = REPO_ROOT / "src" / "db" / "datasets"
API_PATH = REPO_ROOT / "ollama_key.txt"
