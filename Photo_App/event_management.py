import streamlit as st
import qrcode
from pathlib import Path
from io import BytesIO
import urllib.parse

from config import DATA_DIR

BASE_URL = "http://localhost:8501"
QR_DIR = DATA_DIR / "qr_codes"
EVENTS_DIR = DATA_DIR / "events"

QR_DIR.mkdir(exist_ok=True)
EVENTS_DIR.mkdir(exist_ok=True)

def generate_qr(event_name):
    event_url = f"{BASE_URL}?event={urllib.parse.quote(event_name)}"

    qr = qrcode.make(event_url)
    qr_path = QR_DIR / f"{event_name}.png"
    qr.save(qr_path)

    return qr_path

def save_photo(event_name, uploaded_file):
    event_dir = EVENTS_DIR / event_name
    event_dir.mkdir(exist_ok=True)

    file_path = event_dir / uploaded_file.name
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return file_path

def get_event_photos(event_name):
    event_dir = EVENTS_DIR / event_name
    if not event_dir.exists():
        return []
    return list(event_dir.glob("*"))

def event_manager():
    st.title("Event Photo Manager")

    event_name = st.text_input("Event Name")

    if st.button("Generate QR") and event_name:
        qr_path = generate_qr(event_name)
        st.image(str(qr_path))
        st.success("QR code generated")

    uploaded = st.file_uploader("Upload Photo", type=["jpg", "jpeg", "png"])

    if uploaded and event_name:
        path = save_photo(event_name, uploaded)
        st.success(f"Saved: {path.name}")

    if event_name:
        photos = get_event_photos(event_name)
        for photo in photos:
            st.image(str(photo), width=200)

if __name__ == "__main__":
    event_manager()