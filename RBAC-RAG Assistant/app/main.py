from fastapi import FastAPI

from app.routes import chat
from app.auth import routes as auth_routes
from app.core.document_loader import load_documents
from app.core.embedding_engine import build_vector_index

app = FastAPI(
    title="RBAC RAG Internal Chatbot",
    description="""
    A secure internal knowledge assistant that enforces role-based access control (RBAC)
    while retrieving relevant information using vector search.
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url=None
)

app.include_router(auth_routes.router, prefix="/auth")
app.include_router(chat.router)

@app.on_event("startup")
def startup():
    load_documents()
    build_vector_index()