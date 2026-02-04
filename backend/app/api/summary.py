from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.message import Message
from app.services.gemini_service import summarize_conversation

router = APIRouter(prefix="/summary", tags=["Summary"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("")
def generate_summary(
    conversation_id: str,
    target_language: str = "English",
    db: Session = Depends(get_db)
):
    """
    Generate a summary of a conversation.
    
    Query Parameters:
    - conversation_id: ID of the conversation to summarize
    - target_language: Language for the summary (default: English)
    """
    try:
        messages = db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).all()

        if not messages:
            raise HTTPException(status_code=404, detail="Conversation not found")

        # Build conversation text with both original and translated for context
        conversation_text = "\n".join(
            [f"{m.role}: {m.original_text}" for m in messages]
        )

        if not conversation_text.strip():
            return {
                "summary": "No conversation content to summarize.",
                "conversation_id": conversation_id,
                "message_count": 0
            }

        # Generate summary with target language preference
        summary = summarize_conversation(conversation_text, target_language)
        
        return {
            "summary": summary,
            "conversation_id": conversation_id,
            "message_count": len(messages),
            "target_language": target_language
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating summary: {str(e)}")
