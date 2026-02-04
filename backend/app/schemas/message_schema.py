from pydantic import BaseModel
from typing import Optional

class MessageCreate(BaseModel):
    conversation_id: str
    role: str
    source_language: str
    target_language: str
    text: str

class MessageResponse(BaseModel):
    id: str
    conversation_id: str
    role: str
    original_text: str
    translated_text: str
    audio_path: Optional[str]

    class Config:
        orm_mode = True
