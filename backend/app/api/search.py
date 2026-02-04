from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.message import Message

router = APIRouter(prefix="/search", tags=["Search"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("")
def search_messages(
    query: str,
    conversation_id: str = None,
    db: Session = Depends(get_db)
):
    """
    Search for messages by keywords.
    
    Query Parameters:
    - query: Search term (required) - searches in both original and translated text
    - conversation_id: Optional filter for specific conversation
    """
    try:
        if not query or not query.strip():
            raise HTTPException(status_code=400, detail="Query parameter is required")
        
        search_term = f"%{query}%"
        
        # Build base query
        base_query = db.query(Message).filter(
            (Message.original_text.ilike(search_term)) |
            (Message.translated_text.ilike(search_term))
        )
        
        # Filter by conversation if provided
        if conversation_id:
            base_query = base_query.filter(Message.conversation_id == conversation_id)
        
        results = base_query.order_by(Message.created_at.desc()).all()
        
        if not results:
            return {
                "query": query,
                "conversation_id": conversation_id,
                "results": [],
                "total": 0
            }
        
        return {
            "query": query,
            "conversation_id": conversation_id,
            "results": [
                {
                    "id": msg.id,
                    "conversation_id": msg.conversation_id,
                    "role": msg.role,
                    "original_text": msg.original_text,
                    "translated_text": msg.translated_text,
                    "audio_path": msg.audio_path,
                    "timestamp": msg.created_at.isoformat() if msg.created_at else None
                }
                for msg in results
            ],
            "total": len(results)
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching messages: {str(e)}")

@router.get("/conversation/{conversation_id}")
def search_conversation(
    conversation_id: str,
    query: str = None,
    db: Session = Depends(get_db)
):
    """
    Get all messages in a conversation, optionally filtered by search query.
    """
    try:
        base_query = db.query(Message).filter(Message.conversation_id == conversation_id)
        
        if query and query.strip():
            search_term = f"%{query}%"
            base_query = base_query.filter(
                (Message.original_text.ilike(search_term)) |
                (Message.translated_text.ilike(search_term))
            )
        
        messages = base_query.order_by(Message.created_at).all()
        
        if not messages:
            return {
                "conversation_id": conversation_id,
                "query": query,
                "messages": [],
                "total": 0
            }
        
        return {
            "conversation_id": conversation_id,
            "query": query,
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
        raise HTTPException(status_code=500, detail=f"Error retrieving conversation: {str(e)}")
