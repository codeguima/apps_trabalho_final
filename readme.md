
```markdown
# Sistema de Mensageria com Microserviços

## Arquitetura




Sistema completo de autenticação e troca de mensagens com 3 APIs especializadas.

## 📦 Tecnologias

**php-api** (PHP):
- ✅ JWT Authentication
- ✅ Redis (Token Storage)


**python-api** (Python):
- 🐍 Flask
- 🐇 RabbitMQ (Message Queue)
- 🐬 MySQL (Message Storage)
- ✅ MySQL (message Data)

**node-api** (Node.js):
- 🚀 Express
- ✅ MySQL (User Data)
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

Usaro arquivo postman.json, importar no app para testar(mais facil)

## 🌐 Portas dos Serviços

| Serviço               | Porta   | URL                     |
|-----------------------|---------|-------------------------|
| (PHP)                 | 8000    | http://localhost:8000   |
| (Python)              | 5000    | http://localhost:5000   |
| (Node)                | 3000    | http://localhost:3000   |
| MySQL                 | 3306    | -                       |
| Redis                 | 6379    | -                       |
| RabbitMQ Management   | 15672   | http://localhost:15672  |

