import yaml
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

def load_config():
    config_path = BASE_DIR / "configs/base.yaml"
    with open(config_path, "r") as f:
        return yaml.safe_load(f)