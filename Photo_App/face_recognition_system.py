import os
import cv2
import psycopg2
import numpy as np
import gc
from deepface import DeepFace
from retinaface import RetinaFace
from tqdm import tqdm
from PIL import Image

from config import ORIGINALS_DIR

# Database config (unchanged, but centralized here)
DB_PARAMS = {
    "dbname": "kavu_rojasara",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5432",
}

def connect_db():
    return psycopg2.connect(**DB_PARAMS)

def store_embeddings(batch_data):
    if not batch_data:
        return

    conn = connect_db()
    cur = conn.cursor()

    cur.executemany("""
        INSERT INTO face_embeddings (image_path, face_id, embedding)
        VALUES (%s, %s, %s)
        ON CONFLICT (image_path, face_id) DO NOTHING;
    """, [
        (img_path, face_id, embedding.tolist())
        for img_path, face_id, embedding in batch_data
    ])

    conn.commit()
    cur.close()
    conn.close()

def process_image(img_path):
    img = cv2.imread(img_path)
    if img is None:
        return None

    faces = RetinaFace.detect_faces(img_path)
    if not faces:
        return None

    results = []

    for face_index, face_data in enumerate(faces.values()):
        x, y, w, h = face_data["facial_area"]

        expand = 0.1
        x = max(0, x - int(w * expand))
        y = max(0, y - int(h * expand))
        w = min(img.shape[1], w + int(w * expand))
        h = min(img.shape[0], h + int(h * expand))

        face_img = img[y:h, x:w]
        face_img = cv2.resize(face_img, (150, 150))

        embedding_data = DeepFace.represent(
            img_path=face_img,
            model_name="Facenet",
            enforce_detection=False
        )

        if embedding_data:
            embedding = np.array(
                embedding_data[0]["embedding"],
                dtype=np.float32
            )
            if embedding.shape == (128,):
                results.append((img_path, face_index, embedding))

    return results if results else None

def process_images():
    image_files = [
        str(ORIGINALS_DIR / f)
        for f in os.listdir(ORIGINALS_DIR)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ]

    if not image_files:
        print("No images found in data/originals/")
        return

    batch = []

    for img_path in tqdm(image_files):
        results = process_image(img_path)
        if results:
            batch.extend(results)

        if len(batch) >= 50:
            store_embeddings(batch)
            batch.clear()
            gc.collect()

    if batch:
        store_embeddings(batch)

    print("Embeddings processing complete.")

if __name__ == "__main__":
    process_images()