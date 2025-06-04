# Funções de tratamento de erros e decodificação de JWT

from jose import jwt, JWTError, ExpiredSignatureError # type: ignore
import os
from dotenv import load_dotenv # type: ignore

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")

if not JWT_SECRET:
    raise EnvironmentError("JWT_SECRET não está definido nas variáveis de ambiente")

def decode_jwt(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user_id = payload.get("userId")
        if not user_id:
            # Token válido, mas sem userId no payload
            raise ValueError("userId não encontrado no token")
        return user_id
    except ExpiredSignatureError:
        print("Erro: Token expirado")
        return None
    except JWTError:
        print("Erro: Token inválido")
        return None
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return None
