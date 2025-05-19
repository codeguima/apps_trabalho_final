import jwt
import redis
import requests
from functools import wraps
from flask import request, jsonify
from datetime import datetime, timedelta

class AuthService:
    def __init__(self):
        # Configurações (deveriam vir de variáveis de ambiente)
        self.JWT_SECRET = 'your_jwt_secret_here'
        self.JWT_ALGORITHM = 'HS256'
        self.JWT_EXP_DELTA_SECONDS = 86400  # 24 horas
        self.REDIS_HOST = 'localhost'
        self.REDIS_PORT = 6379
        self.AUTH_API_URL = 'http://auth-api/api'
        
        # Conexão com Redis
        self.redis = redis.Redis(
            host=self.REDIS_HOST,
            port=self.REDIS_PORT,
            decode_responses=True
        )

    def generate_token(self, user_id):
        """Gera um novo token JWT para o usuário"""
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(seconds=self.JWT_EXP_DELTA_SECONDS),
            'iat': datetime.utcnow()
        }
        token = jwt.encode(payload, self.JWT_SECRET, algorithm=self.JWT_ALGORITHM)
        self._store_token(user_id, token)
        return token

    def validate_token(self, token):
        """Valida um token JWT"""
        if not token:
            return False

        try:
            # Verifica primeiro no cache local (Redis)
            user_id = self._get_user_id_from_token(token)
            if not user_id:
                return False

            cached_token = self.redis.get(f"user_token:{user_id}")
            if cached_token == token:
                return True

            # Se não encontrou no cache, verifica na Auth-API
            response = requests.post(
                f"{self.AUTH_API_URL}/validate",
                json={'token': token},
                headers={'Content-Type': 'application/json'},
                timeout=2
            )

            if response.status_code == 200 and response.json().get('valid'):
                self._store_token(user_id, token)
                return True

            return False
        except Exception as e:
            print(f"Token validation error: {str(e)}")
            return False

    def get_current_user(self, token):
        """Obtém o usuário atual a partir do token"""
        if not token:
            return None

        try:
            # Remove 'Bearer ' se presente
            token = token.replace('Bearer ', '')
            
            payload = jwt.decode(
                token,
                self.JWT_SECRET,
                algorithms=[self.JWT_ALGORITHM],
                options={'verify_exp': True}
            )
            return payload.get('user_id')
        except jwt.ExpiredSignatureError:
            print("Token expirado")
            return None
        except jwt.InvalidTokenError:
            print("Token inválido")
            return None
        except Exception as e:
            print(f"Error getting current user: {str(e)}")
            return None

    def auth_required(self, f):
        """Decorator para proteger endpoints que requerem autenticação"""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = request.headers.get('Authorization')
            
            if not token or not self.validate_token(token):
                return jsonify({
                    'status': 'error',
                    'message': 'Acesso não autorizado'
                }), 401
                
            return f(*args, **kwargs)
        return decorated_function

    def _store_token(self, user_id, token):
        """Armazena o token no Redis"""
        try:
            self.redis.setex(
                f"user_token:{user_id}",
                self.JWT_EXP_DELTA_SECONDS,
                token
            )
        except Exception as e:
            print(f"Error storing token in Redis: {str(e)}")

    def _get_user_id_from_token(self, token):
        """Obtém o user_id do token sem validar (apenas decode)"""
        try:
            payload = jwt.decode(
                token,
                options={"verify_signature": False},
                algorithms=[self.JWT_ALGORITHM]
            )
            return payload.get('user_id')
        except:
            return None

    def invalidate_token(self, user_id):
        """Invalida o token do usuário"""
        try:
            return self.redis.delete(f"user_token:{user_id}") > 0
        except Exception as e:
            print(f"Error invalidating token: {str(e)}")
            return False