import time
import numpy as np
import faiss

from src.utils.config import load_config
from src.utils.paths import get_artifact_dir


def main():
    config = load_config()
    faiss_cfg = config["faiss"]

    artifact_dir = get_artifact_dir()

    # Load embeddings and labels
    gallery_emb = np.load(artifact_dir / "gallery_embeddings.npy").astype("float32")
    query_emb = np.load(artifact_dir / "query_embeddings.npy").astype("float32")
    gallery_labels = np.load(artifact_dir / "gallery_labels.npy")
    query_labels = np.load(artifact_dir / "query_labels.npy")

    # Load FAISS index
    index = faiss.read_index(str(artifact_dir / "gallery.index"))

    if faiss_cfg["index_type"] == "ivf":
        index.nprobe = faiss_cfg["nprobe"]

    # ---- FAISS search timing ----
    start = time.time()
    _, indices = index.search(query_emb, 10)
    end = time.time()

    avg_query_time = (end - start) / len(query_emb)
    print(f"Avg FAISS query time: {avg_query_time:.6f} sec")

    # ---- Recall computation ----
    retrieved_labels = gallery_labels[indices]

    for k in [1, 5, 10]:
        correct = 0
        for i in range(len(query_labels)):
            if query_labels[i] in retrieved_labels[i, :k]:
                correct += 1
        recall = correct / len(query_labels)
        print(f"FAISS Recall@{k}: {recall:.4f}")


if __name__ == "__main__":
    main()