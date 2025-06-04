# FastAPI app, endpoints e lifecycle

from fastapi import FastAPI, Request # type: ignore
from contextlib import asynccontextmanager
import asyncio

from consumer import consume
from redis_client import redis_client
from models import MessagePayload
from auth import validate_token
from rabbitmq import publish_message

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(consume())
    yield
    await redis_client.close()
    print("Desligando app...")

app = FastAPI(lifespan=lifespan)

@app.post("/send-message")
async def send_message(request: Request, payload: MessagePayload):
    token = request.headers.get("Authorization")
    user_id = await validate_token(token)

    message = {
        "from_user_id": user_id,
        "to_user_id": payload.to_user_id,
        "message": payload.message
    }

    await publish_message(message)

    return {"status": "Mensagem enviada com sucesso"}
