from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

from app.core.document_loader import get_all_documents
from config.company_structure import get_accessible_departments

model = SentenceTransformer("all-MiniLM-L6-v2")

vector_index = None
chunk_store = []


def chunk_text(text, chunk_size=120):
    words = text.split()
    return [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]


def build_vector_index():
    global vector_index, chunk_store

    documents = get_all_documents()

    embeddings = []
    chunk_store = []

    for doc in documents:
        chunks = chunk_text(doc["content"])

        for chunk in chunks:
            chunk_store.append({
                "text": chunk,
                "department": doc["department"],
                "doc_id": doc["id"]
            })

            emb = model.encode(chunk)
            embeddings.append(emb)

    embeddings = np.array(embeddings).astype("float32")

    dim = embeddings.shape[1]
    vector_index = faiss.IndexFlatL2(dim)
    vector_index.add(embeddings)

    print(f"Vector index built with {len(chunk_store)} chunks")


def search_chunks(query, role, k=10, score_threshold=0.3):
    accessible_departments = get_accessible_departments(role)

    query_embedding = model.encode([query]).astype("float32")
    distances, indices = vector_index.search(query_embedding, k)

    results = []

    query_lower = query.lower()
    query_words = query_lower.split()

    # INTENT CHECK 
    restricted_intent = False
    if "salary" in query_lower and role != "admin":
        restricted_intent = True

    for i, idx in enumerate(indices[0]):
        chunk = chunk_store[idx]

        base_score = 1 / (1 + distances[0][i])

        department = chunk["department"]
        source = chunk["doc_id"].lower()
        text_lower = chunk["text"].lower()

        # RBAC RULES

        # Department access
        if department not in accessible_departments:
            continue

        # Salary restriction 
        if "salary" in source and role != "admin":
            continue

        # Crawling restriction
        if "crawling" in source and role not in ["admin", "manager"]:
            continue

        # KEYWORD BOOST
        boost = 0
        for word in query_words:
            if word in text_lower:
                boost += 0.1

        score = base_score + boost

        if score > score_threshold:
            results.append({
                "text": chunk["text"],
                "score": float(score),
                "source": chunk["doc_id"]
            })

    # If restricted intent → return nothing 
    if restricted_intent:
        return []

    results = sorted(results, key=lambda x: x["score"], reverse=True)

    return results[:3]