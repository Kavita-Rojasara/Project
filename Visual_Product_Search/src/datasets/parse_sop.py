import os
import pandas as pd

RAW_DATA_DIR = "data/raw/stanford_online_products"

def parse_metadata():
    records = []

    for file in os.listdir(RAW_DATA_DIR):
        if not file.endswith(".txt"):
            continue

        category = file.replace("_final.txt", "")
        file_path = os.path.join(RAW_DATA_DIR, file)

        with open(file_path, "r") as f:
            for line in f.readlines()[1:]:  # skip header
                parts = line.strip().split()
                if len(parts) < 4:
                    continue

                image_id = parts[0]
                product_id = parts[1]
                image_rel_path = parts[-1]

                image_full_path = os.path.join(RAW_DATA_DIR, image_rel_path)

                records.append({
                    "image_id": image_id,
                    "product_id": product_id,
                    "category": category,
                    "image_path": image_full_path
                })

    df = pd.DataFrame(records)
    return df

if __name__ == "__main__":
    df = parse_metadata()
    print(df.head())
    print("Total images:", len(df))
    print("Unique products:", df["product_id"].nunique())