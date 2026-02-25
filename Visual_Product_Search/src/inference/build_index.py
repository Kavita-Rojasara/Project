import numpy as np
import faiss
from src.utils.config import load_config

config = load_config()
faiss_cfg = config["faiss"]

gallery_emb = np.load("artifacts/gallery_embeddings.npy").astype("float32")
dim = gallery_emb.shape[1]

index_type = faiss_cfg["index_type"]

if index_type == "flat":
    index = faiss.IndexFlatIP(dim)

elif index_type == "ivf":
    nlist = faiss_cfg["nlist"]
    quantizer = faiss.IndexFlatIP(dim)
    index = faiss.IndexIVFFlat(quantizer, dim, nlist, faiss.METRIC_INNER_PRODUCT)
    index.train(gallery_emb)

else:
    raise ValueError(f"Unknown FAISS index type: {index_type}")

index.add(gallery_emb)

faiss.write_index(index, "artifacts/gallery.index")
print(f"FAISS index built using type: {index_type}")