import os
from fastapi import HTTPException
import httpx

API_NODE_URL = os.getenv("API_NODE_URL")

async def validate_token(token: str):
    if not token or not token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token inválido")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{API_NODE_URL}/me",
                headers={"Authorization": token},
                timeout=5.0,
            )

        if response.status_code != 200:
            raise HTTPException(status_code=401, detail="Token inválido ou expirado")

        user_data = response.json()
        user_id = user_data.get("id")

        if not user_id:
            raise HTTPException(status_code=401, detail="Usuário inválido ou sem ID")

        return int(user_id)

    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Erro de comunicação com servidor de autenticação: {e}")
