# Pydantic models

from pydantic import BaseModel

class MessagePayload(BaseModel):
    to_user_id: int
    message: str
