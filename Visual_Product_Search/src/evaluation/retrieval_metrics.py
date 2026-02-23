import numpy as np
import faiss

def recall_at_k(query_emb, query_labels, gallery_emb, gallery_labels, k=1):
    index = faiss.IndexFlatIP(gallery_emb.shape[1])
    index.add(gallery_emb)

    scores, indices = index.search(query_emb, k)

    correct = 0
    for i, idxs in enumerate(indices):
        if query_labels[i] in [gallery_labels[j] for j in idxs]:
            correct += 1

    return correct / len(query_labels)