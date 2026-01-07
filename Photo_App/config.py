from pathlib import Path

# Project root = Photo_App/
BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
ORIGINALS_DIR = DATA_DIR / "originals"
FACES_DIR = DATA_DIR / "faces"
EMBEDDINGS_DIR = DATA_DIR / "embeddings"

# Ensure directories exist
for d in [DATA_DIR, ORIGINALS_DIR, FACES_DIR, EMBEDDINGS_DIR]:
    d.mkdir(parents=True, exist_ok=True)