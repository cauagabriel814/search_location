# API de Localização por Coordenadas

API REST segura para buscar informações de localidade a partir de coordenadas geográficas (latitude e longitude) usando OpenStreetMap Nominatim.

## 📋 Índice

- [Características](#características)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Autenticação](#autenticação)
- [Endpoints](#endpoints)
- [Deploy com Docker](#deploy-com-docker)
- [Exemplos Práticos](#exemplos-práticos)
- [Segurança](#segurança)
- [Troubleshooting](#troubleshooting)

## ✨ Características

- ✅ **Autenticação JWT** - Tokens seguros com expiração configurável
- ✅ **Rate Limiting** - Proteção contra abuso (10 req/hora padrão)
- ✅ **Validação de Coordenadas** - Latitude (-90 a 90) e Longitude (-180 a 180)
- ✅ **Documentação Automática** - Swagger UI e ReDoc integrados
- ✅ **Geocoding Reverso** - OpenStreetMap Nominatim (gratuito)
- ✅ **Docker Ready** - Dockerfile e docker-compose incluídos
- ✅ **Health Checks** - Monitoramento de saúde da aplicação

## 🚀 Instalação

### Opção 1: Instalação Local

1. **Clone o repositório**
```bash
git clone <seu-repo>
cd api_procurar_localidade
```

2. **Crie e ative o ambiente virtual**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Configure o arquivo `.env`**
```bash
cp .env.example .env
# Edite o .env com suas configurações
```

### Opção 2: Docker (Recomendado)

```bash
# Build e iniciar
docker-compose up -d --build

# Verificar status
docker-compose ps

# Ver logs
docker-compose logs -f
```

## ⚙️ Configuração

### Arquivo `.env`

Crie o arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
# Configuração JWT
JWT_SECRET=minha-chave-secreta-super-segura-2024
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# Credenciais de Autenticação
API_USERNAME=admin
API_PASSWORD=sua-senha-forte

# Rate Limiting
RATE_LIMIT=10/hour
```

**⚠️ IMPORTANTE em Produção:**
- Mude `JWT_SECRET` para um valor aleatório e forte
- Use senha complexa em `API_PASSWORD`
- Nunca commite o arquivo `.env` no Git (já está no `.gitignore`)

### Variáveis de Ambiente

| Variável | Descrição | Padrão | Obrigatória |
|----------|-----------|--------|-------------|
| `JWT_SECRET` | Chave secreta para assinar tokens JWT | - | ✅ Sim |
| `JWT_ALGORITHM` | Algoritmo de criptografia JWT | HS256 | ❌ Não |
| `JWT_EXPIRATION_HOURS` | Tempo de expiração do token (horas) | 24 | ❌ Não |
| `API_USERNAME` | Nome de usuário para autenticação | - | ✅ Sim |
| `API_PASSWORD` | Senha para autenticação | - | ✅ Sim |
| `RATE_LIMIT` | Limite de requisições | 10/hour | ❌ Não |
| `PORT` | Porta da aplicação | 8000 | ❌ Não |

## 🔐 Autenticação

A API usa autenticação **JWT (JSON Web Tokens)**. Você precisa:

### 1. Obter um Token

**Endpoint:** `POST /auth/token`

**Request:**
```bash
curl -X POST "http://localhost:8000/auth/token" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "sua-senha"
  }'
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTc1OTUyMTMzN30.xFT6Vm7BOC-VLoKZDaf5ARBK7vl-GnbJ6MsBIrbtalI",
  "token_type": "bearer",
  "expires_in": 86400
}
```

- **access_token**: O token JWT que você usará nas próximas requisições
- **token_type**: Sempre será "bearer"
- **expires_in**: Tempo de expiração em segundos (24h = 86400s)

### 2. Usar o Token

Inclua o token no header `Authorization` de todas as requisições protegidas:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 3. Token Expirado

Se o token expirar, você receberá:

```json
{
  "detail": "Token inválido ou expirado"
}
```

Nesse caso, gere um novo token repetindo o passo 1.

## 📍 Endpoints

### `GET /` - Raiz da API

Retorna informações sobre a API.

**Request:**
```bash
curl http://localhost:8000/
```

**Response:**
```json
{
  "message": "API de Localização por Coordenadas",
  "version": "1.0.0",
  "endpoints": {
    "auth": "/auth/token - POST - Gera token JWT",
    "localidade": "/localidade?lat={lat}&lng={lng} - GET - Busca localidade (requer JWT)"
  }
}
```

---

### `POST /auth/token` - Gerar Token JWT

Gera um token de autenticação válido.

**Headers:**
```
Content-Type: application/json
```

**Body:**
```json
{
  "username": "admin",
  "password": "sua-senha"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 86400
}
```

**Response (401 Unauthorized):**
```json
{
  "detail": "Credenciais inválidas"
}
```

---

### `GET /localidade` - Buscar Localidade

Busca informações de endereço a partir de coordenadas geográficas.

**🔒 Requer Autenticação**

**Headers:**
```
Authorization: Bearer {seu_token}
```

**Query Parameters:**

| Parâmetro | Tipo | Descrição | Validação | Obrigatório |
|-----------|------|-----------|-----------|-------------|
| `lat` | float | Latitude | -90 a 90 | ✅ Sim |
| `lng` | float | Longitude | -180 a 180 | ✅ Sim |

**Request:**
```bash
curl -X GET "http://localhost:8000/localidade?lat=-23.5505&lng=-46.6333" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Response (200 OK):**
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

**Response (401 Unauthorized) - Sem token:**
```json
{
  "detail": "Not authenticated"
}
```

**Response (404 Not Found) - Coordenadas inválidas:**
```json
{
  "detail": "Localização não encontrada para as coordenadas fornecidas"
}
```

**Response (422 Unprocessable Entity) - Validação falhou:**
```json
{
  "detail": [
    {
      "loc": ["query", "lat"],
      "msg": "ensure this value is greater than or equal to -90",
      "type": "value_error.number.not_ge"
    }
  ]
}
```

**Response (429 Too Many Requests) - Rate limit excedido:**
```json
{
  "detail": "Rate limit exceeded: 10 per 1 hour"
}
```

**Response (503 Service Unavailable) - Serviço indisponível:**
```json
{
  "detail": "Serviço de geolocalização temporariamente indisponível. Tente novamente."
}
```

## 🐳 Deploy com Docker

### Estrutura de Arquivos Docker

```
├── Dockerfile           # Imagem da aplicação
├── docker-compose.yml   # Orquestração
└── .dockerignore       # Arquivos ignorados no build
```

### Comandos Docker

#### Build e Iniciar
```bash
docker-compose up -d --build
```

#### Ver Logs
```bash
# Todos os logs
docker-compose logs -f

# Últimas 100 linhas
docker-compose logs --tail=100 -f
```

#### Verificar Status
```bash
docker-compose ps
```

#### Parar Aplicação
```bash
docker-compose down
```

#### Reiniciar
```bash
docker-compose restart
```

#### Reconstruir Imagem
```bash
docker-compose build --no-cache
docker-compose up -d
```

### Deploy em Nuvem

#### AWS EC2

1. **Criar instância EC2** (Ubuntu 22.04)
2. **Conectar via SSH**
3. **Instalar Docker:**
```bash
sudo apt update
sudo apt install docker.io docker-compose -y
sudo systemctl start docker
sudo systemctl enable docker
```

4. **Upload dos arquivos:**
```bash
scp -r * usuario@ip-publico:/home/usuario/api
```

5. **No servidor:**
```bash
cd /home/usuario/api
sudo docker-compose up -d --build
```

6. **Abrir porta 8000 no Security Group**

7. **Acessar:** `http://SEU_IP_PUBLICO:8000`

#### Google Cloud Run

```bash
# Build
gcloud builds submit --tag gcr.io/SEU_PROJECT/api-localidade

# Deploy
gcloud run deploy api-localidade \
  --image gcr.io/SEU_PROJECT/api-localidade \
  --platform managed \
  --allow-unauthenticated \
  --set-env-vars JWT_SECRET=sua-chave,API_USERNAME=admin,API_PASSWORD=senha
```

#### Railway / Render

1. Conecte seu repositório GitHub
2. Configure as variáveis de ambiente no painel
3. Deploy automático

## 📚 Exemplos Práticos

### Python

```python
import requests

# 1. Obter token
auth_response = requests.post(
    "http://localhost:8000/auth/token",
    json={"username": "admin", "password": "admin123"}
)
token = auth_response.json()["access_token"]

# 2. Buscar localidade
headers = {"Authorization": f"Bearer {token}"}
response = requests.get(
    "http://localhost:8000/localidade",
    params={"lat": -23.5505, "lng": -46.6333},
    headers=headers
)

print(response.json())
```

### JavaScript (Node.js)

```javascript
const axios = require('axios');

async function buscarLocalidade() {
  // 1. Obter token
  const authRes = await axios.post('http://localhost:8000/auth/token', {
    username: 'admin',
    password: 'admin123'
  });

  const token = authRes.data.access_token;

  // 2. Buscar localidade
  const response = await axios.get('http://localhost:8000/localidade', {
    params: { lat: -23.5505, lng: -46.6333 },
    headers: { Authorization: `Bearer ${token}` }
  });

  console.log(response.data);
}

buscarLocalidade();
```

### cURL

```bash
# 1. Obter token e salvar em variável
TOKEN=$(curl -s -X POST "http://localhost:8000/auth/token" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' \
  | grep -o '"access_token":"[^"]*"' \
  | cut -d'"' -f4)

# 2. Usar o token
curl -X GET "http://localhost:8000/localidade?lat=-23.5505&lng=-46.6333" \
  -H "Authorization: Bearer $TOKEN"
```

### PowerShell

```powershell
# 1. Obter token
$auth = Invoke-RestMethod -Uri "http://localhost:8000/auth/token" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"username":"admin","password":"admin123"}'

$token = $auth.access_token

# 2. Buscar localidade
$headers = @{ Authorization = "Bearer $token" }
$response = Invoke-RestMethod -Uri "http://localhost:8000/localidade?lat=-23.5505&lng=-46.6333" `
  -Headers $headers

$response | ConvertTo-Json
```

## 🔒 Segurança

### Implementações de Segurança

- ✅ **Autenticação JWT obrigatória** - Todos os endpoints protegidos
- ✅ **Rate Limiting por IP** - Proteção contra DDoS
- ✅ **Validação de entrada** - Coordenadas validadas
- ✅ **Tratamento de erros** - Mensagens seguras
- ✅ **Secrets em variáveis** - Credenciais não hardcoded
- ✅ **HTTPS Ready** - Use proxy reverso em produção
- ✅ **CORS configurável** - Controle de origem

### Boas Práticas em Produção

1. **Use HTTPS** - Configure nginx/caddy como proxy reverso
2. **Mude credenciais** - Nunca use as padrão em produção
3. **JWT_SECRET forte** - Mínimo 32 caracteres aleatórios
4. **Firewall** - Feche portas desnecessárias
5. **Logs centralizados** - Use CloudWatch, Datadog, etc
6. **Backups** - Configure backups automáticos
7. **Monitoring** - Configure alertas (Uptimerobot, etc)
8. **Rate limit ajustado** - Configure conforme necessidade

### Exemplo Nginx (HTTPS)

```nginx
server {
    listen 443 ssl;
    server_name api.seudominio.com;

    ssl_certificate /etc/letsencrypt/live/seudominio.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/seudominio.com/privkey.pem;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 📖 Documentação Interativa

Após iniciar a aplicação, acesse:

- **Swagger UI**: http://localhost:8000/docs
  - Interface interativa para testar endpoints
  - Documentação automática com exemplos
  - Teste direto no navegador

- **ReDoc**: http://localhost:8000/redoc
  - Documentação mais limpa e organizada
  - Melhor para leitura

## 🔧 Troubleshooting

### Erro: "Not authenticated"

**Causa:** Token ausente ou inválido

**Solução:**
1. Gere um novo token em `/auth/token`
2. Certifique-se de incluir `Authorization: Bearer {token}` no header

---

### Erro: "Token inválido ou expirado"

**Causa:** Token expirou (padrão 24h)

**Solução:** Gere um novo token

---

### Erro: "Credenciais inválidas"

**Causa:** Username/password incorretos

**Solução:** Verifique o `.env` e use as credenciais corretas

---

### Erro: "Rate limit exceeded"

**Causa:** Limite de requisições excedido

**Solução:**
1. Aguarde 1 hora ou
2. Aumente o `RATE_LIMIT` no `.env`

---

### Container não inicia

**Diagnóstico:**
```bash
docker-compose logs api
```

**Causas comuns:**
- Arquivo `.env` não existe
- Variáveis obrigatórias faltando
- Porta 8000 já em uso

**Solução:**
```bash
# Verificar porta em uso
netstat -ano | findstr :8000  # Windows
lsof -i :8000  # Linux/Mac

# Mudar porta no docker-compose.yml
ports:
  - "8080:8000"
```

---

### Localização não encontrada

**Causa:** Coordenadas em área sem mapeamento

**Solução:** Teste com coordenadas conhecidas (ex: São Paulo -23.5505, -46.6333)

---

### Serviço indisponível (503)

**Causa:** Nominatim offline ou timeout

**Solução:**
1. Aguarde alguns minutos
2. Verifique internet
3. Tente novamente

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Versão | Uso |
|------------|--------|-----|
| **FastAPI** | 0.115.0 | Framework web |
| **Uvicorn** | 0.30.6 | Servidor ASGI |
| **Python-Jose** | 3.3.0 | JWT authentication |
| **Geopy** | 2.4.1 | Geocoding (Nominatim) |
| **SlowAPI** | 0.1.9 | Rate limiting |
| **Passlib** | 1.7.4 | Hash de senhas |
| **Pydantic** | 2.x | Validação de dados |

## 📊 Limitações

- **Rate Limit:** 10 requisições/hora por IP (configurável)
- **Nominatim:** Política de uso justo (1 req/segundo máximo)
- **Geocoding:** Depende da qualidade do mapeamento OpenStreetMap
- **Sem histórico:** Não armazena consultas anteriores

## 📄 Licença

MIT License - Sinta-se livre para usar em projetos pessoais e comerciais.

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir melhorias
- Enviar pull requests

---

**Desenvolvido com ❤️ usando FastAPI**
