# função para consumir e salvar mensagens no Redis

import asyncio
import ast
from config import QUEUE_NAME
from redis_client import redis_client
import aio_pika # type: ignore

async def consume():
    for attempt in range(10):
        try:
            print(f"Tentando conectar ao RabbitMQ (tentativa {attempt+1})...")
            connection = await aio_pika.connect_robust()
            break
        except Exception as e:
            print(f"Erro ao conectar ao RabbitMQ: {e}")
            await asyncio.sleep(5)
    else:
        print("Não foi possível conectar ao RabbitMQ após várias tentativas.")
        return

    channel = await connection.channel()
    queue = await channel.declare_queue(QUEUE_NAME, durable=True)

    print("Conectado e aguardando mensagens...")

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                try:
                    data = ast.literal_eval(message.body.decode())
                    from_id = data["from_user_id"]
                    to_id = data["to_user_id"]
                    msg = data["message"]
                    key = f"messages:from:{from_id}:to:{to_id}"
                    await redis_client.lpush(key, msg)
                    print(f"Mensagem salva em Redis key={key}")
                except Exception as e:
                    print("Erro ao processar mensagem:", e)
