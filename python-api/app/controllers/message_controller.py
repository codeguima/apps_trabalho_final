from flask import request, jsonify
from services.rabbitmq_service import RabbitMQService
from services.auth_service import AuthService
from models.message import Message

class MessageController:
    def __init__(self):
        self.rabbitmq = RabbitMQService()
        self.auth = AuthService()

    def store_message(self):
        data = request.get_json()
        token = request.headers.get('Authorization')

        if not self.auth.validate_token(token):
            return jsonify({"status": "error", "message": "Unauthorized"}), 401

        message = Message(
            sender_id=data['sender_id'],
            receiver_id=data['receiver_id'],
            content=data['content']
        )
        message.save()

        # Publica no RabbitMQ para a Receive-Send-API processar
        self.rabbitmq.publish_message({
            "type": "new_message",
            "message_id": message.id,
            "token": token
        })

        return jsonify({"status": "success", "message_id": message.id}), 200

    def get_messages(self, user_id):
        token = request.headers.get('Authorization')
        
        if not self.auth.validate_token(token):
            return jsonify({"status": "error", "message": "Unauthorized"}), 401

        messages = Message.get_by_user(user_id)
        return jsonify({"status": "success", "messages": messages}), 200