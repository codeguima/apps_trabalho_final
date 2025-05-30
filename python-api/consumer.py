import asyncio
import os
import ast
from dotenv import load_dotenv
import aio_pika
import redis.asyncio as redis

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
RABBITMQ_URL = os.getenv("RABBITMQ_URL")
QUEUE_NAME = os.getenv("QUEUE_NAME")

async def consume():
  while True:
    print("Consumindo mensagens...")
    
    redisConnection = redis.Redis(
      host=REDIS_HOST,
      port=int(REDIS_PORT),
      password=REDIS_PASSWORD,
      decode_responses=True
    )
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    channel = await connection.channel()
    queue = await channel.declare_queue(QUEUE_NAME, durable=True)

    async with queue.iterator() as queue_iter:
      async for message in queue_iter:
        async with message.process():
          try:
            data = ast.literal_eval(message.body.decode())
            from_id = data["from_user_id"]
            to_id = data["to_user_id"]
            msg = data["message"]
            key = f"messages:from:{from_id}:to:{to_id}"
            await redisConnection.lpush(key, msg)
            print(f"Mensagem salva em Redis key={key}")
          except Exception as e:
            print("Erro ao processar mensagem:", e)