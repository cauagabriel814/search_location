# Guia Docker - API de Localização

## Pré-requisitos

1. **Instalar Docker Desktop**
   - Windows: https://docs.docker.com/desktop/install/windows-install/
   - Mac: https://docs.docker.com/desktop/install/mac-install/
   - Linux: https://docs.docker.com/engine/install/

2. **Iniciar Docker Desktop**
   - Abra o Docker Desktop e aguarde até estar rodando

3. **Verificar instalação**
```bash
docker --version
docker-compose --version
```

## Como Usar

### Opção 1: Docker Compose (Recomendado)

```bash
# Build e iniciar
docker-compose up -d --build

# Ver logs
docker-compose logs -f

# Verificar status
docker-compose ps

# Parar
docker-compose down
```

### Opção 2: Docker Manual

```bash
# Build da imagem
docker build -t api-localidade .

# Rodar container
docker run -d \
  -p 8000:8000 \
  --name api-localidade \
  --env-file .env \
  api-localidade

# Ver logs
docker logs -f api-localidade

# Parar
docker stop api-localidade
docker rm api-localidade
```

## Testar a API

Após iniciar, teste:

```bash
# 1. Verificar se está rodando
curl http://localhost:8000/

# 2. Gerar token
curl -X POST http://localhost:8000/auth/token \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# 3. Buscar localidade (substitua SEU_TOKEN)
curl -X GET "http://localhost:8000/localidade?lat=-23.5505&lng=-46.6333" \
  -H "Authorization: Bearer SEU_TOKEN"
```

## Melhorias no Dockerfile

### O que foi adicionado:

1. **Variáveis de ambiente Python**
   - `PYTHONUNBUFFERED=1` - Output imediato dos logs
   - `PYTHONDONTWRITEBYTECODE=1` - Não criar arquivos .pyc
   - `PIP_NO_CACHE_DIR=1` - Reduzir tamanho da imagem

2. **Curl instalado**
   - Necessário para o health check

3. **Usuário não-root**
   - Mais seguro rodar como usuário `appuser`

4. **Health check**
   - Verifica se a aplicação está respondendo
   - Usado pelo Docker e Kubernetes

## Comandos Úteis

```bash
# Ver todos os containers rodando
docker ps

# Ver logs específicos
docker logs api-localidade

# Acessar terminal do container
docker exec -it api-localidade sh

# Ver uso de recursos
docker stats

# Remover imagens antigas
docker image prune -a

# Rebuild sem cache
docker-compose build --no-cache
docker-compose up -d
```

## Troubleshooting

### Erro: "Cannot connect to Docker daemon"

**Causa:** Docker Desktop não está rodando

**Solução:**
1. Abra o Docker Desktop
2. Aguarde inicializar completamente
3. Tente novamente

---

### Erro: "port is already allocated"

**Causa:** Porta 8000 já está em uso

**Solução 1:** Parar o que está usando a porta
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :8000
kill <PID>
```

**Solução 2:** Mudar a porta no docker-compose.yml
```yaml
ports:
  - "8080:8000"  # Usar porta 8080 externa
```

---

### Erro: ".env file not found"

**Causa:** Arquivo .env não existe

**Solução:**
```bash
cp .env.example .env
# Edite o .env com suas configurações
```

---

### Container inicia mas não responde

**Diagnóstico:**
```bash
docker logs api-localidade
```

**Possíveis causas:**
- Variáveis de ambiente faltando
- Erro na aplicação
- Dependências não instaladas

---

### Rebuild completo

Se nada funcionar, reconstrua tudo do zero:

```bash
# Parar e remover tudo
docker-compose down -v
docker system prune -a

# Rebuild
docker-compose up -d --build
```

## Deploy em Produção

### Registries

**Docker Hub:**
```bash
docker tag api-localidade:latest seuusuario/api-localidade:latest
docker push seuusuario/api-localidade:latest
```

**AWS ECR:**
```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin SEU_ECR_URI
docker tag api-localidade:latest SEU_ECR_URI/api-localidade:latest
docker push SEU_ECR_URI/api-localidade:latest
```

**Google Container Registry:**
```bash
docker tag api-localidade:latest gcr.io/SEU_PROJECT/api-localidade:latest
docker push gcr.io/SEU_PROJECT/api-localidade:latest
```

## Otimizações

### Multi-stage build (opcional)

Se quiser uma imagem ainda menor:

```dockerfile
# Stage 1: Build
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY app.py auth.py ./
ENV PATH=/root/.local/bin:$PATH
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Segurança

- ✅ Usuário não-root
- ✅ Imagem slim (menor superfície de ataque)
- ✅ Health checks
- ✅ Secrets via variáveis de ambiente
- ✅ Sem arquivos desnecessários (.dockerignore)

## Monitoramento

Adicionar ao docker-compose.yml:

```yaml
services:
  api:
    # ... configuração existente
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

Isso limita os logs a 3 arquivos de 10MB cada.
