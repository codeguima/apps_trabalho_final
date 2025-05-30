from fastapi import FastAPI, Request, HTTPException, Depends
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import os
import aio_pika
import redis.asyncio as redis
from utils.jwt_utils import decode_jwt
from pydantic import BaseModel
import asyncio
from consumer import consume

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
RABBITMQ_URL = os.getenv("RABBITMQ_URL")
QUEUE_NAME = os.getenv("QUEUE_NAME")

class MessagePayload(BaseModel):
  to_user_id: int
  message: str

def get_redis():
  return redis.Redis(
    host=REDIS_HOST,
    port=int(REDIS_PORT),
    password=REDIS_PASSWORD,
    decode_responses=True
  )

app = FastAPI()
redis_client: redis.Redis = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global redis_client
    redis_client = redis.Redis(
      host=os.getenv("REDIS_HOST"),
      port=int(os.getenv("REDIS_PORT")),
      password=os.getenv("REDIS_PASSWORD"),
      decode_responses=True
    )

    asyncio.create_task(consume())
    
    yield
    
    await redis_client.close()

    print("Desligando app...")

app = FastAPI(lifespan=lifespan)

@app.post("/send-message")
async def send_message(request: Request, payload: MessagePayload):
  token = request.headers.get("Authorization")
  if not token or not token.startswith("Bearer "):
    raise HTTPException(status_code=401, detail="Token inválido")

  token_value = token.split(" ")[1]

  token_key = f"user:token:{token_value}"

  # Valida token no Redis
  if not await redis_client.exists(token_key):
    raise HTTPException(status_code=401, detail="Token expirado ou inválido")

  # Decodifica JWT
  user_id = decode_jwt(token_value)
  if not user_id:
    raise HTTPException(status_code=401, detail="Token JWT inválido")

  # Publica mensagem no RabbitMQ
  connection = await aio_pika.connect_robust(RABBITMQ_URL)
  async with connection:
    channel = await connection.channel()
    queue = await channel.declare_queue(QUEUE_NAME, durable=True)
    message = {
      "from_user_id": int(user_id),
      "to_user_id": payload.to_user_id,
      "message": payload.message
    }
    await channel.default_exchange.publish(
      aio_pika.Message(body=str(message).encode()),
      routing_key=queue.name,
    )

  return {"status": "Mensagem enviada com sucesso"}
