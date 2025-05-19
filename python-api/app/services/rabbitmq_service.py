import pika
import json
from services.auth_service import AuthService

class RabbitMQService:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='message_queue')
        self.auth = AuthService()

    def publish_message(self, message):
        if not self.auth.validate_token(message.get('token')):
            return {"status": "error", "message": "Invalid token"}

        self.channel.basic_publish(
            exchange='',
            routing_key='message_queue',
            body=json.dumps(message)
        )
        return {"status": "success", "message": "Message published"}

    def consume_messages(self, callback):
        def wrapped_callback(ch, method, properties, body):
            message = json.loads(body)
            if self.auth.validate_token(message.get('token')):
                callback(message)
            else:
                print("Invalid token, message rejected")

        self.channel.basic_consume(
            queue='message_queue',
            on_message_callback=wrapped_callback,
            auto_ack=True
        )
        self.channel.start_consuming()