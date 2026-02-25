from fastapi import FastAPI, UploadFile, File, HTTPException
from PIL import Image
import io

from src.inference.search import ImageSearchEngine

app = FastAPI(title="Visual Product Search")

# --- Initialize engine safely ---
try:
    engine = ImageSearchEngine()
except Exception as e:
    engine = None
    init_error = str(e)


@app.post("/search")
async def search_image(
    file: UploadFile = File(...),
    k: int = 5
):
    if engine is None:
        raise HTTPException(
            status_code=500,
            detail=f"Search engine not initialized: {init_error}"
        )

    if k <= 0:
        raise HTTPException(
            status_code=400,
            detail="k must be a positive integer"
        )

    # --- Load image safely ---
    try:
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is not a valid image"
        )

    # --- Run search ---
    try:
        results = engine.search(image, k)
        return {
            "top_k": k,
            "results": results
        }
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Inference failed: {str(e)}"
        )