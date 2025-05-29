from flask import Blueprint, jsonify, request
from .models import Message
from .extensions import db, cache
import json
from datetime import datetime

bp = Blueprint('main', __name__)

@bp.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    required_fields = ['message', 'user_id_send', 'user_id_received']

    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Campos obrigatórios faltando'}), 400

    try:
        message = Message(
            message=data['message'],
            user_id_send=data['user_id_send'],
            user_id_received=data['user_id_received']
        )
        db.session.add(message)
        db.session.commit()

        cache.delete('all_messages')

        return jsonify(message.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/messages', methods=['GET'])
def list_messages():
    cached_data = cache.get('all_messages')
    if cached_data:
        return jsonify(json.loads(cached_data))

    messages = Message.query.all()
    result = [msg.to_dict() for msg in messages]

    cache.set('all_messages', json.dumps(result), ex=300)

    return jsonify(result)

@bp.route('/messages/<int:id>', methods=['GET'])
def get_message(id):
    message = Message.query.get_or_404(id)
    return jsonify(message.to_dict())

@bp.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    cache.delete('all_messages')
    return jsonify({'message': 'Mensagem deletada com sucesso'})

@bp.route('/healthcheck', methods=['GET'])
def healthcheck():
    try:
        db.engine.execute('SELECT 1')
        cache.cache._client.ping()
        return jsonify({'status': 'healthy'})
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500
