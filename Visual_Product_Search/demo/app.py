import streamlit as st
import requests
from PIL import Image
import io

# -------------------------
# Configuration
# -------------------------

API_URL = "http://127.0.0.1:8000/search"

st.set_page_config(page_title="Visual Product Search", layout="wide")

st.title("Visual Product Search Demo")

st.markdown(
    "Upload an image and retrieve visually similar products "
    "using a trained embedding model + FAISS index."
)

# -------------------------
# Sidebar Controls
# -------------------------

k = st.sidebar.slider("Number of results (k)", min_value=1, max_value=10, value=5)

uploaded_file = st.file_uploader(
    "Upload Query Image",
    type=["jpg", "jpeg", "png"]
)

# -------------------------
# Main Logic
# -------------------------

if uploaded_file is not None:
    try:
        query_image = Image.open(uploaded_file).convert("RGB")
    except Exception:
        st.error("Uploaded file is not a valid image.")
        st.stop()

    st.subheader("Query Image")
    st.image(query_image, use_container_width=True)

    st.markdown("---")

    files = {
        "file": (
            uploaded_file.name,
            uploaded_file.getvalue(),
            uploaded_file.type
        )
    }

    # -------------------------
    # API Request (SAFE)
    # -------------------------

    try:
        response = requests.post(
            API_URL,
            files=files,
            params={"k": k},
            timeout=15
        )
        response.raise_for_status()

    except requests.exceptions.ConnectionError:
        st.error("Backend is not running. Please start FastAPI first.")
        st.stop()

    except requests.exceptions.Timeout:
        st.error("Backend request timed out.")
        st.stop()

    except requests.exceptions.HTTPError:
        try:
            detail = response.json().get("detail", "Unknown backend error")
        except Exception:
            detail = "Unknown backend error"
        st.error(f"Backend error: {detail}")
        st.stop()

    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
        st.stop()

    # -------------------------
    # Parse Response
    # -------------------------

    data = response.json()

    if "results" not in data:
        st.error("Invalid response from backend.")
        st.stop()

    results = data["results"]

    if len(results) == 0:
        st.warning("No results returned.")
        st.stop()

    # -------------------------
    # Display Results
    # -------------------------

    st.subheader("Retrieved Results")

    cols = st.columns(len(results))

    for col, item in zip(cols, results):
        image_path = item.get("image_path")
        similarity = item.get("similarity")
        product_id = item.get("product_id")

        if image_path is None:
            continue

        try:
            result_img = Image.open(image_path).convert("RGB")
            col.image(result_img, use_container_width=True)

            col.markdown(f"**Product ID:** {product_id}")
            if similarity is not None:
                col.markdown(f"**Similarity:** {similarity:.3f}")

        except Exception:
            col.warning("Failed to load image.")