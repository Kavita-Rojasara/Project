import pandas as pd
from sklearn.model_selection import train_test_split
from parse_sop import parse_metadata

def create_splits():
    df = parse_metadata()

    gallery_rows = []
    query_rows = []

    for product_id, group in df.groupby("product_id"):
        if len(group) < 2:
            continue  # cannot split

        gallery, query = train_test_split(
            group,
            test_size=0.3,
            random_state=42
        )

        gallery_rows.append(gallery)
        query_rows.append(query)

    gallery_df = pd.concat(gallery_rows)
    query_df = pd.concat(query_rows)

    gallery_df.to_csv("data/splits/gallery.csv", index=False)
    query_df.to_csv("data/splits/query.csv", index=False)

    print("Gallery images:", len(gallery_df))
    print("Query images:", len(query_df))

if __name__ == "__main__":
    create_splits()