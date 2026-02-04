from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.sql import func
from app.db.base import Base
import uuid

class Message(Base):
    __tablename__ = "messages"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id = Column(String)
    role = Column(String)
    original_text = Column(Text)
    translated_text = Column(Text)
    audio_path = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
