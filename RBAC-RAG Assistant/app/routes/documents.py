from fastapi import APIRouter, Depends, HTTPException
from jose import jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.document_loader import get_all_documents
from app.core.security import SECRET_KEY, ALGORITHM

router = APIRouter()
security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.get("/documents")
def get_documents(user=Depends(get_current_user)):
    role = user["role"]

    docs = get_all_documents()

    allowed_docs = [
        {
            "id": d["id"],
            "department": d["department"],
            "filename": d["filename"]
        }
        for d in docs
        if role in d["allowed_roles"]
    ]

    return {
        "user_role": role,
        "accessible_documents": allowed_docs
    }