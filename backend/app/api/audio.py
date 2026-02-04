from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.message import Message
from app.services.gemini_service import translate_text, transcribe_audio
import uuid
import os
from pathlib import Path

router = APIRouter(prefix="/audio", tags=["Audio"])

UPLOAD_DIR = "uploads/audio"
Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("")
async def upload_audio(
    conversation_id: str = Form(...),
    role: str = Form(...),
    source_language: str = Form(...),
    target_language: str = Form(...),
    audio: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload audio file, transcribe it, translate, and save to conversation.
    
    Form Parameters:
    - conversation_id: ID of the conversation
    - role: "doctor" or "patient"
    - source_language: Language of the audio
    - target_language: Language to translate to
    - audio: Audio file (webm, mp3, wav, etc.)
    """
    try:
        # Validate input
        if role not in ["doctor", "patient"]:
            raise HTTPException(status_code=400, detail="Role must be 'doctor' or 'patient'")
        
        # Generate unique filename
        file_ext = Path(audio.filename).suffix if audio.filename else ".webm"
        filename = f"{uuid.uuid4()}{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        # Save audio file
        try:
            contents = await audio.read()
            with open(file_path, "wb") as f:
                f.write(contents)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error saving audio file: {str(e)}")
        
        # Transcribe audio to text
        transcribed_text = ""
        try:
            transcribed_text = transcribe_audio(file_path)
            if not transcribed_text or not transcribed_text.strip():
                raise HTTPException(status_code=400, detail="Could not transcribe audio. Please check the audio file.")
        except Exception as e:
            # If transcription fails, return error (don't save incomplete message)
            os.remove(file_path)  # Clean up the file
            raise HTTPException(status_code=500, detail=f"Transcription error: {str(e)}")
        
        # Translate transcribed text
        try:
            translated_text = translate_text(
                transcribed_text,
                source_language,
                target_language
            )
        except Exception as e:
            os.remove(file_path)
            raise HTTPException(status_code=500, detail=f"Translation error: {str(e)}")
        
        # Create message record with audio
        try:
            msg = Message(
                conversation_id=conversation_id,
                role=role,
                original_text=transcribed_text,
                translated_text=translated_text,
                audio_path=f"uploads/audio/{filename}"
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
        except Exception as e:
            db.rollback()
            os.remove(file_path)
            raise HTTPException(status_code=500, detail=f"Error saving message: {str(e)}")
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.get("/{message_id}")
def get_audio(message_id: str, db: Session = Depends(get_db)):
    """
    Retrieve audio file information for a specific message.
    """
    try:
        msg = db.query(Message).filter(Message.id == message_id).first()
        
        if not msg or not msg.audio_path:
            raise HTTPException(status_code=404, detail="Audio not found")
        
        if not os.path.exists(msg.audio_path):
            raise HTTPException(status_code=404, detail="Audio file not found on disk")
        
        return {
            "id": msg.id,
            "audio_path": msg.audio_path,
            "original_text": msg.original_text,
            "translated_text": msg.translated_text,
            "role": msg.role,
            "timestamp": msg.created_at.isoformat() if msg.created_at else None
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving audio: {str(e)}")
