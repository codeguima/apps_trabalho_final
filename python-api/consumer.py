import pika
import json
from db import SessionLocal, engine
from models import Message, Base

# Cria tabelas se não existirem
Base.metadata.create_all(bind=engine)

# Conexão com o RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()
channel.queue_declare(queue='messages')

def callback(ch, method, properties, body):
    data = json.loads(body)
    session = SessionLocal()
    try:
        msg = Message(
            message=data['message'],
            user_id_send=data['user_id_send'],
            user_id_received=data['user_id_received']
        )
        session.add(msg)
        session.commit()
        print(f"Mensagem salva: {data}")
    except Exception as e:
        print("Erro ao salvar mensagem:", e)
        session.rollback()
    finally:
        session.close()

channel.basic_consume(queue='messages', on_message_callback=callback, auto_ack=True)

print('🎧 Aguardando mensagens...')
channel.start_consuming()
# Fechando a conexão com o RabbitMQ ao finalizar
connection.close()