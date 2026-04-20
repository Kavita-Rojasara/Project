from fastapi import APIRouter, Depends

from app.auth.routes import get_current_user
from app.core.embedding_engine import search_chunks
from app.core.answer_generator import generate_answer

router = APIRouter()


@router.post("/chat")
def chat(query: str, user=Depends(get_current_user)):
    role = user["role"]

    results = search_chunks(query, role)

    if not results:
        return {
            "query": query,
            "answer": "I couldn’t find a clear answer in the available documents.",
            "sources": []
        }

    answer = generate_answer(query, results)

    sources = [results[0]["source"]]

    return {
        "query": query,
        "answer": answer,
        "sources": sources
    }