# Data

## Overview

This directory defines the dataset structure used for the Visual Product Search system.

Large image files and processed data are intentionally **not committed to version control** to keep the repository lightweight and reproducible.

This folder documents how data should be organized locally.

---

## Directory Structure

```text
data/
├── raw/           # Original dataset images (gitignored)
├── processed/     # Resized or transformed images (gitignored)
├── splits/        # CSV files defining gallery and query splits
└── README.md
```

---

## raw/

This directory contains the original dataset images.

Expected example structure:

```text
data/raw/
└── stanford_online_products/
    ├── bicycle_final/
    ├── chair_final/
    ├── table_final/
    └── ...
```

These files are **not committed** because:

- The dataset is large
- It can be downloaded independently
- It is reproducible

If the dataset is missing, training and embedding extraction will not work.

---

## processed/

This directory is used for any intermediate preprocessing steps, such as:

- Resized images
- Cropped images
- Normalized image copies
- Augmented images

This folder is optional and depends on your preprocessing pipeline.

All contents inside this directory are gitignored.

---

## splits/

This directory contains small CSV files defining dataset splits.

Example:

```text
data/splits/
├── gallery.csv
└── query.csv
```

Each CSV typically contains:

- image_path  
- product_id  

These files define:

- Which images belong to the gallery set  
- Which images are used as query inputs  

The split design directly affects Recall@K evaluation.

---

## Dataset Used

This project was developed using the **Stanford Online Products** dataset.

The dataset must be downloaded separately and placed inside:

```text
data/raw/
```

No dataset files are included in this repository.

---

## Reproducibility

To fully reproduce experiments:

1. Download the dataset.
2. Place it inside `data/raw/`.
3. Ensure `gallery.csv` and `query.csv` are present in `data/splits/`.
4. Run training and embedding extraction scripts.

All downstream artifacts (embeddings and FAISS index) are generated automatically.

---

## Important Notes

- Do not commit large datasets to version control.
- Keep raw and processed data separated.
- Splits should remain lightweight and versioned.
- Changing dataset structure requires regenerating embeddings and FAISS index.