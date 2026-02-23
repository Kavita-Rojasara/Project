from pathlib import Path
from src.utils.config import load_config

BASE_DIR = Path(__file__).resolve().parents[2]

def get_artifact_dir():
    config = load_config()
    model_name = config["model"]["backbone"]
    return BASE_DIR / "artifacts" / model_name