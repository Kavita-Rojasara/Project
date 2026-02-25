# Artifacts

## Overview

This directory stores all generated outputs from model training, embedding extraction, and FAISS index construction.

Artifacts are intentionally **not committed to version control** because they are:

- Large in size  
- Fully reproducible  
- Configuration-dependent  
- Specific to backbone experiments  

All files in this folder can be regenerated using scripts inside the `src/` directory.

---

## Directory Structure

```text
artifacts/
├── resnet18/
│   ├── embedding_model.pt        # Trained metric learning model
│   ├── gallery_embeddings.npy    # Gallery image embeddings
│   ├── query_embeddings.npy      # Query image embeddings
│   ├── gallery_labels.npy        # Gallery product IDs
│   ├── query_labels.npy          # Query product IDs
│   └── gallery.index             # FAISS index built from gallery embeddings
│
├── resnet50/
│   ├── embedding_model.pt
│   ├── gallery_embeddings.npy
│   ├── query_embeddings.npy
│   ├── gallery_labels.npy
│   ├── query_labels.npy
│   └── gallery.index
```

Each backbone has its own isolated artifact folder to prevent experiment mixing and ensure reproducibility.

---

## File Descriptions

**embedding_model.pt**  
Saved model weights after metric learning.  
Used for embedding extraction and API inference.

**gallery_embeddings.npy**  
NumPy array containing embedding vectors for all gallery images.  
Shape: `(num_gallery_images, embedding_dim)`

**query_embeddings.npy**  
NumPy array containing embedding vectors for all query images.  
Shape: `(num_query_images, embedding_dim)`

**gallery_labels.npy**  
Ground-truth product IDs corresponding to gallery embeddings.  
Used for Recall@K evaluation.

**query_labels.npy**  
Ground-truth product IDs corresponding to query embeddings.  
Used for Recall@K evaluation.

**gallery.index**  
FAISS index built from `gallery_embeddings.npy`.  
Used for fast nearest neighbor search during evaluation and API inference.

---

## How Artifacts Are Generated

Artifacts are generated in three sequential stages.

The active configuration is defined in:

```text
configs/base.yaml
```

Changing the backbone or index type requires regenerating artifacts.

---

### Step 1 — Train the Model

```bash
python -m src.training.train
```

Generates:
- `embedding_model.pt`

Saved under the backbone-specific artifact folder.

---

### Step 2 — Extract Embeddings

```bash
python -m src.evaluation.extract_embeddings
```

Generates:
- `gallery_embeddings.npy`
- `query_embeddings.npy`
- `gallery_labels.npy`
- `query_labels.npy`

---

### Step 3 — Build FAISS Index

```bash
python -m src.inference.build_index
```

Generates:
- `gallery.index`

The FAISS index type (Flat or IVF) is controlled via `configs/base.yaml`.

---

## Important Notes

- Artifacts must match the selected backbone configuration.
- Switching backbones requires retraining and re-extracting embeddings.
- Changing FAISS index type requires rebuilding the index.
- Artifacts are environment-specific and should not be manually edited.
- If artifacts are missing, the API will fail safely with a clear error message.

---

## Reproducibility

This project is designed to remain lightweight and reproducible.

To rebuild the entire system from scratch:

1. Train  
2. Extract embeddings  
3. Build FAISS index  

No manual artifact modification is required.