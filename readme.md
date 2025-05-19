
```markdown
# Sistema de Mensageria com Microserviços

## Arquitetura



Sistema completo de autenticação e troca de mensagens com 3 APIs especializadas.

## 📦 Tecnologias

**Auth-API** (PHP):
- ✅ JWT Authentication
- ✅ Redis (Token Storage)
- ✅ MySQL (User Data)

**Record-API** (Python):
- 🐍 Flask
- 🐇 RabbitMQ (Message Queue)
- 🐬 MySQL (Message Storage)

**Receive-Send-API** (Node.js):
- 🚀 Express
- 🔄 RabbitMQ Consumer
- 🔒 JWT Validation

## 🚀 Instalação Rápida

1. Clone o repositório:
```bash
git clone https://github.com/codeguima/apps_trabalho_final.git
cd apps_trabalho_final
```

2. Inicie os containers:
```bash
docker-compose up -d --build
```

## 🔌 Endpoints Principais

### Autenticação
```http
POST /api/register
Content-Type: application/json

{
  "name": "Usuário Teste",
  "email": "teste@email.com",
  "password": "senha123"
}
```

### Mensagens
```http
POST /api/messages
Authorization: Bearer <token>
Content-Type: application/json

{
  "receiverId": 2,
  "content": "Olá mundo!"
}
```

## 🌐 Portas dos Serviços

| Serviço               | Porta   | URL                     |
|-----------------------|---------|-------------------------|
| Auth-API (PHP)        | 8000    | http://localhost:8000   |
| Record-API (Python)   | 5000    | http://localhost:5000   |
| Receive-Send-API (Node)| 3000   | http://localhost:3000   |
| MySQL                 | 3306    | -                       |
| Redis                 | 6379    | -                       |
| RabbitMQ Management   | 15672   | http://localhost:15672  |

## 🐳 Docker Compose

```yaml
version: '3.8'

services:
  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: message_system
  
  redis:
    image: redis:alpine

  rabbitmq:
    image: rabbitmq:management

  auth-api:
    build: ./auth-api
    ports: ["8000:80"]

  record-api:
    build: ./record-api
    ports: ["5000:5000"]

  receive-send-api:
    build: ./receive-send-api
    ports: ["3000:3000"]
```

## 📊 Fluxo de Dados

1. Cliente envia mensagem → Receive-Send-API (Node)
2. Valida token → Auth-API (PHP)
3. Armazena mensagem → Record-API (Python)
4. Publica evento → RabbitMQ
5. Notifica destinatário ← Consumer (Node)

## ⚙️ Variáveis de Ambiente

Crie um arquivo `.env` na raiz:

```ini
JWT_SECRET=sua_chave_super_secreta
MYSQL_HOST=db
REDIS_HOST=redis
RABBITMQ_HOST=rabbitmq
```

## 🧪 Testando

```bash
# Registrar usuário
curl -X POST http://localhost:8000/api/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Teste","email":"teste@email.com","password":"123"}'

# Enviar mensagem (substitua TOKEN)
curl -X POST http://localhost:3000/api/messages \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"receiverId":2,"content":"Teste"}'
```

## 📂 Estrutura de Arquivos

```
.
├── auth-api/          # PHP (Autenticação)
├── record-api/        # Python (Armazenamento)
├── receive-send-api/  # Node.js (Gerenciamento)
├── docker-compose.yml
└── README.md
```

## 🛑 Comandos Úteis

| Comando               | Descrição                     |
|-----------------------|-------------------------------|
| `docker-compose up`   | Inicia todos os serviços      |
| `docker-compose logs` | Mostra logs dos containers    |
| `docker-compose down` | Para e remove os containers   |


