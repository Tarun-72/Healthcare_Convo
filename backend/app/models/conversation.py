from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from app.db.base import Base
import uuid

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
