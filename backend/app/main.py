from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.api import chat, audio, search, summary
from app.db.session import engine
from app.db.base import Base

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Healthcare Conversation Translator",
    description="Real-time translation and AI-powered summarization for doctor-patient conversations",
    version="1.0.0"
)

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve uploaded audio files
uploads_dir = "uploads"
if not os.path.exists(uploads_dir):
    os.makedirs(uploads_dir, exist_ok=True)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Include API routers
app.include_router(chat.router)
app.include_router(audio.router)
app.include_router(search.router)
app.include_router(summary.router)

# Health check endpoint
@app.get("/health")
def health_check():
    """
    Health check endpoint for monitoring.
    """
    return {
        "status": "healthy",
        "service": "Healthcare Conversation Translator",
        "version": "1.0.0"
    }

@app.get("/")
def root():
    """
    API root endpoint.
    """
    return {
        "message": "Healthcare Conversation Translator API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }
