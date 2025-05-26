from sqlalchemy import Column, Integer, String
from db import Base

class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, index=True)
    message = Column(String(500))
    user_id_send = Column(Integer)
    user_id_received = Column(Integer)
