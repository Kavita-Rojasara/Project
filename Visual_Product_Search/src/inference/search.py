import torch
import numpy as np
import faiss
import pandas as pd
from PIL import Image
from torchvision import transforms
from pathlib import Path

from src.models.embedder import ResNetEmbedder
from src.utils.config import load_config
from src.utils.paths import get_artifact_dir


class ImageSearchEngine:
    def __init__(self):
        self.device = "cpu"

        config = load_config()
        artifact_dir = get_artifact_dir()

        model_path = artifact_dir / "embedding_model.pt"
        index_path = artifact_dir / "gallery.index"
        gallery_csv = Path("data/splits/gallery.csv")

        # --- Safety checks ---
        if not model_path.exists():
            raise RuntimeError(
                f"Model not found at {model_path}. Run training first."
            )

        if not index_path.exists():
            raise RuntimeError(
                f"FAISS index not found at {index_path}. Run build_index first."
            )

        if not gallery_csv.exists():
            raise RuntimeError(
                "Gallery metadata not found. Ensure data splits exist."
            )

        # --- Load model ---
        self.model = ResNetEmbedder(embedding_dim=256).to(self.device)
        self.model.load_state_dict(
            torch.load(model_path, map_location=self.device)
        )
        self.model.eval()

        # --- Load FAISS index ---
        self.index = faiss.read_index(str(index_path))

        faiss_cfg = config["faiss"]
        if faiss_cfg["index_type"] == "ivf":
            self.index.nprobe = faiss_cfg["nprobe"]

        # --- Load metadata ---
        self.gallery_df = pd.read_csv(gallery_csv)

        # --- Image transforms ---
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])

        print(f"ImageSearchEngine initialized using artifacts from: {artifact_dir}")

    def search(self, image: Image.Image, k: int = 5):
        if k <= 0:
            raise ValueError("k must be greater than 0")

        if k > len(self.gallery_df):
            raise ValueError("k exceeds gallery size")

        # --- Preprocess ---
        image = self.transform(image).unsqueeze(0).to(self.device)

        # --- Embed ---
        with torch.no_grad():
            embedding = self.model(image).cpu().numpy().astype("float32")

        # --- FAISS search ---
        distances, indices = self.index.search(embedding, k)

        # --- Build response ---
        results = []
        for score, idx in zip(distances[0], indices[0]):
            row = self.gallery_df.iloc[idx]
            results.append({
                "product_id": int(row["product_id"]),
                "image_path": row["image_path"],
                "similarity": float(score)
            })

        return results