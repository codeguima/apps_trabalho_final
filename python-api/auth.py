# funções para lidar com autenticação JWT

from fastapi import HTTPException # type: ignore
from redis_client import redis_client
from utils.jwt_utils import decode_jwt

async def validate_token(token: str):
    if not token or not token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token inválido")

    token_value = token.split(" ")[1]
    token_key = f"user:token:{token_value}"

    if not await redis_client.exists(token_key):
        raise HTTPException(status_code=401, detail="Token expirado ou inválido")

    user_id = decode_jwt(token_value)
    if not user_id:
        raise HTTPException(status_code=401, detail="Token JWT inválido")

    return int(user_id)
