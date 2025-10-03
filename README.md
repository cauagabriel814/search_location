# API de Localização por Coordenadas

API REST para buscar informações de localidade a partir de coordenadas geográficas (latitude e longitude).

## 🌐 URL da API

```
https://external-projects-api-localization.zq8ms6.easypanel.host
```

## 🔑 Autenticação

Token fixo (enviar no header):
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTc1OTUyMTMzN30.xFT6Vm7BOC-VLoKZDaf5ARBK7vl-GnbJ6MsBIrbtalI
```

## 📍 Endpoint

### GET /localidade

**URL:**
```
https://external-projects-api-localization.zq8ms6.easypanel.host/localidade?lat={lat}&lng={lng}
```

**Parâmetros:**
- `lat` - Latitude (-90 a 90)
- `lng` - Longitude (-180 a 180)

**Exemplo de Requisição:**
```bash
curl -X GET "https://external-projects-api-localization.zq8ms6.easypanel.host/localidade?lat=-23.5505&lng=-46.6333" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTc1OTUyMTMzN30.xFT6Vm7BOC-VLoKZDaf5ARBK7vl-GnbJ6MsBIrbtalI"
```

## 📤 Resposta

A API retorna um JSON com as seguintes informações:

```json
{
  "endereco": "Sé, Rua Santa Teresa, Glicério, Sé, São Paulo, Região Imediata de São Paulo, Região Metropolitana de São Paulo, Região Geográfica Intermediária de São Paulo, São Paulo, Região Sudeste, 01016-020, Brasil",
  "bairro": "Glicério",
  "cidade": "São Paulo",
  "estado": "São Paulo",
  "pais": "Brasil",
  "cep": "01016-020",
  "coordenadas": {
    "lat": -23.5505,
    "lng": -46.6333
  }
}
```

### Campos Retornados

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `endereco` | string | Endereço completo |
| `bairro` | string | Bairro/Distrito |
| `cidade` | string | Cidade/Município |
| `estado` | string | Estado/Província |
| `pais` | string | País |
| `cep` | string | Código postal |
| `coordenadas` | object | Latitude e longitude enviadas |

**Nota:** Alguns campos podem retornar `null` se a informação não estiver disponível no OpenStreetMap.

## 📚 Exemplos de Coordenadas

| Local | Latitude | Longitude |
|-------|----------|-----------|
| São Paulo, Brasil | -23.5505 | -46.6333 |
| Rio de Janeiro, Brasil | -22.9068 | -43.1729 |
| Nova York, EUA | 40.7128 | -74.0060 |
| Londres, Reino Unido | 51.5074 | -0.1278 |
| Paris, França | 48.8566 | 2.3522 |
| Tóquio, Japão | 35.6762 | 139.6503 |

## 🐳 Deploy com Docker

```bash
# Build e iniciar
docker-compose up -d --build

# Ver logs
docker-compose logs -f

# Parar
docker-compose down
```

## ⚙️ Configuração (.env)

```env
API_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTc1OTUyMTMzN30.xFT6Vm7BOC-VLoKZDaf5ARBK7vl-GnbJ6MsBIrbtalI
RATE_LIMIT=10/hour
```

## 📖 Documentação Interativa

- **Swagger UI**: https://external-projects-api-localization.zq8ms6.easypanel.host/docs

## ⚡ Rate Limit

- 10 requisições por hora por IP

## 🛠️ Tecnologias

- FastAPI
- OpenStreetMap Nominatim (geocoding gratuito)
- Docker
