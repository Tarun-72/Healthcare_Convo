from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.message import Message
from app.services.gemini_service import translate_text
from app.schemas.message_schema import MessageCreate, MessageResponse

router = APIRouter(prefix="/messages", tags=["Chat"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("")
def send_message(data: MessageCreate, db: Session = Depends(get_db)):
    """
    Send a message and get real-time translation.
    
    Request Body:
    - conversation_id: ID of the conversation
    - role: "doctor" or "patient"
    - source_language: Language the user is typing in
    - target_language: Language to translate to
    - text: The message text
    """
    try:
        # Validate input
        if not data.text or not data.text.strip():
            raise HTTPException(status_code=400, detail="Message text cannot be empty")
        
        if data.role not in ["doctor", "patient"]:
            raise HTTPException(status_code=400, detail="Role must be 'doctor' or 'patient'")
        
        # Translate the message
        translated = translate_text(
            data.text,
            data.source_language,
            data.target_language
        )

        # Save message to database
        msg = Message(
            conversation_id=data.conversation_id,
            role=data.role,
            original_text=data.text,
            translated_text=translated
        )

        db.add(msg)
        db.commit()
        db.refresh(msg)

        return {
            "message": {
                "id": msg.id,
                "conversation_id": msg.conversation_id,
                "role": msg.role,
                "original_text": msg.original_text,
                "translated_text": msg.translated_text,
                "audio_path": msg.audio_path,
                "timestamp": msg.created_at.isoformat() if msg.created_at else None
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error sending message: {str(e)}")

@router.get("/{conversation_id}")
def get_conversation_messages(conversation_id: str, db: Session = Depends(get_db)):
    """
    Retrieve all messages in a conversation.
    """
    try:
        messages = db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at).all()

        return {
            "conversation_id": conversation_id,
            "messages": [
                {
                    "id": msg.id,
                    "conversation_id": msg.conversation_id,
                    "role": msg.role,
                    "original_text": msg.original_text,
                    "translated_text": msg.translated_text,
                    "audio_path": msg.audio_path,
                    "timestamp": msg.created_at.isoformat() if msg.created_at else None
                }
                for msg in messages
            ],
            "total": len(messages)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving messages: {str(e)}")
