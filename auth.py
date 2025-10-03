from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
from dotenv import load_dotenv

load_dotenv()

# Token fixo de autorização
API_TOKEN = os.getenv("API_TOKEN")

# Security scheme
security = HTTPBearer()


def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)) -> bool:
    """Verifica se o token é válido"""
    token = credentials.credentials

    if token != API_TOKEN:
        raise HTTPException(
            status_code=401,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return True
