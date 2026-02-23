import numpy as np
from src.evaluation.retrieval_metrics import recall_at_k

gallery_emb = np.load("artifacts/gallery_embeddings.npy")
query_emb = np.load("artifacts/query_embeddings.npy")
gallery_labels = np.load("artifacts/gallery_labels.npy")
query_labels = np.load("artifacts/query_labels.npy")

for k in [1, 5, 10]:
    r = recall_at_k(query_emb, query_labels, gallery_emb, gallery_labels, k)
    print(f"Recall@{k}: {r:.4f}")