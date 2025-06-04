# funções para conexão e publicar mensagens

import aio_pika
from app.config import RABBITMQ_URL, QUEUE_NAME

async def get_rabbitmq_connection():
    return await aio_pika.connect_robust(RABBITMQ_URL)

async def publish_message(message: dict):
    connection = await get_rabbitmq_connection()
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue(QUEUE_NAME, durable=True)
        await channel.default_exchange.publish(
            aio_pika.Message(body=str(message).encode()),
            routing_key=queue.name,
        )
