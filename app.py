from fastapi import FastAPI, HTTPException, Depends, Request, status, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import os
from dotenv import load_dotenv
from auth import create_access_token, verify_token, verify_credentials

load_dotenv()

# Inicializa o FastAPI
app = FastAPI(
    title="API de Localização por Coordenadas",
    description="API para buscar endereço a partir de latitude e longitude usando OpenStreetMap",
    version="1.0.0"
)

# Configuração de Rate Limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Inicializa o geocoder
geolocator = Nominatim(user_agent="api_procurar_localidade")


# Models
class LoginRequest(BaseModel):
    username: str = Field(..., description="Nome de usuário")
    password: str = Field(..., description="Senha")


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class LocalidadeResponse(BaseModel):
    endereco: str | None = None
    bairro: str | None = None
    cidade: str | None = None
    estado: str | None = None
    pais: str | None = None
    cep: str | None = None
    coordenadas: dict


# Endpoints
@app.get("/")
async def root():
    """Endpoint raiz com informações da API"""
    return {
        "message": "API de Localização por Coordenadas",
        "version": "1.0.0",
        "endpoints": {
            "auth": "/auth/token - POST - Gera token JWT",
            "localidade": "/localidade?lat={lat}&lng={lng} - GET - Busca localidade (requer JWT)"
        }
    }


@app.post("/auth/token", response_model=TokenResponse, tags=["Autenticação"])
async def login(credentials: LoginRequest):
    """
    Gera um token JWT válido para autenticação

    Credenciais padrão (configure no .env):
    - username: admin
    - password: admin123
    """
    if not verify_credentials(credentials.username, credentials.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Cria o token
    access_token = create_access_token(
        data={"sub": credentials.username}
    )

    expiration_hours = int(os.getenv("JWT_EXPIRATION_HOURS", 24))

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": expiration_hours * 3600  # em segundos
    }


@app.get("/localidade", response_model=LocalidadeResponse, tags=["Localização"])
@limiter.limit(os.getenv("RATE_LIMIT", "10/hour"))
async def get_localidade(
    request: Request,
    lat: float = Query(..., ge=-90, le=90, description="Latitude (-90 a 90)"),
    lng: float = Query(..., ge=-180, le=180, description="Longitude (-180 a 180)"),
    token_data: dict = Depends(verify_token)
):
    """
    Busca informações de localidade a partir de coordenadas geográficas

    Requer autenticação JWT via header: Authorization: Bearer {token}

    Parâmetros:
    - lat: Latitude (-90 a 90)
    - lng: Longitude (-180 a 180)

    Retorna informações detalhadas do endereço
    """
    try:
        # Busca a localização usando Nominatim
        location = geolocator.reverse(f"{lat}, {lng}", language="pt", timeout=10)

        if not location:
            raise HTTPException(
                status_code=404,
                detail="Localização não encontrada para as coordenadas fornecidas"
            )

        # Extrai os dados do endereço
        address = location.raw.get("address", {})

        # Monta a resposta
        response = {
            "endereco": location.address,
            "bairro": address.get("suburb") or address.get("neighbourhood") or address.get("quarter"),
            "cidade": address.get("city") or address.get("town") or address.get("village") or address.get("municipality"),
            "estado": address.get("state"),
            "pais": address.get("country"),
            "cep": address.get("postcode"),
            "coordenadas": {
                "lat": lat,
                "lng": lng
            }
        }

        return response

    except GeocoderTimedOut:
        raise HTTPException(
            status_code=503,
            detail="Serviço de geolocalização temporariamente indisponível. Tente novamente."
        )
    except GeocoderServiceError as e:
        raise HTTPException(
            status_code=503,
            detail=f"Erro no serviço de geolocalização: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno do servidor: {str(e)}"
        )


# Handler de erros global
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": f"Erro interno: {str(exc)}"}
    )


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
