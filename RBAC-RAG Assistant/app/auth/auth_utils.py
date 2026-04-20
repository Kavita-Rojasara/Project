from jose import jwt, JWTError
from datetime import datetime, timedelta
from app.models.user import User

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

FAKE_USERS_DB = {
    "admin": {
        "username": "admin",
        "password": "admin123",
        "role": "admin",
        "department": "management"
    },
    "engineer": {
        "username": "engineer",
        "password": "engineer123",
        "role": "employee",
        "department": "engineering"
    },
    "manager": {
        "username": "manager",
        "password": "manager123",
        "role": "manager",
        "department": "ai_data"
    },
    "intern": {
        "username": "intern",
        "password": "intern123",
        "role": "intern",
        "department": "engineering"
    }
}


def authenticate_user(username: str, password: str):
    user = FAKE_USERS_DB.get(username)
    if not user or user["password"] != password:
        return None

    return User(
        username=user["username"],
        role=user["role"],
        department=user["department"]
    )


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None