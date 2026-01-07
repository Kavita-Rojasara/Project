import os
import psycopg2
import numpy as np
import streamlit as st
from deepface import DeepFace
from retinaface import RetinaFace
from PIL import Image
import cv2
import zipfile
import io

DB_PARAMS = {
    "dbname": "kavu_rojasara",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5432",
}

def connect_db():
    return psycopg2.connect(**DB_PARAMS)

def load_embeddings():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT image_path, face_id, embedding FROM face_embeddings")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    paths = []
    embeddings = []

    for path, face_id, emb in rows:
        try:
            # Handle embeddings stored as string "[1.2, 3.4, ...]"
            if isinstance(emb, str):
                emb = emb.strip("[]")
                emb = np.fromstring(emb, sep=",", dtype=np.float32)
            else:
                emb = np.array(emb, dtype=np.float32)

            if emb.shape == (128,):
                paths.append(path)
                embeddings.append(emb)

        except Exception:
            continue

    return paths, np.array(embeddings)

def find_matches(query_embeddings, threshold=0.7):
    paths, stored = load_embeddings()
    results = set()

    for q in query_embeddings:
        sims = np.dot(stored, q) / (
            np.linalg.norm(stored, axis=1) * np.linalg.norm(q)
        )
        for i, sim in enumerate(sims):
            if sim >= threshold:
                results.add(paths[i])

    return list(results)

def create_zip(files):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as zipf:
        for f in files:
            zipf.write(f, arcname=os.path.basename(f))
    buffer.seek(0)
    return buffer

def main():
    st.title("Wedding Photo Finder")

    threshold = st.slider("Similarity Threshold", 0.5, 0.95, 0.7)

    uploads = st.file_uploader(
        "Upload selfie(s)",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True
    )

    query_embeddings = []

    for file in uploads or []:
        image = Image.open(file)
        img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        faces = RetinaFace.detect_faces(img)
        for face in faces.values():
            x, y, w, h = face["facial_area"]
            face_img = cv2.resize(img[y:h, x:w], (150, 150))

            emb = DeepFace.represent(
                face_img,
                model_name="Facenet",
                enforce_detection=False
            )
            query_embeddings.append(
                np.array(emb[0]["embedding"], dtype=np.float32)
            )

    if query_embeddings:
        matches = find_matches(query_embeddings, threshold)

        if matches:
            zip_file = create_zip(matches)
            st.download_button(
                "Download Matches",
                zip_file,
                "matches.zip",
                "application/zip"
            )

            for img in matches:
                st.image(img, use_container_width=True)
        else:
            st.warning("No matches found.")

if __name__ == "__main__":
    main()