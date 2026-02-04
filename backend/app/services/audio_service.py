import os
import uuid
from fastapi import UploadFile

UPLOAD_DIR = "uploads/audio"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_audio_file(audio: UploadFile) -> str:
    filename = f"{uuid.uuid4()}_{audio.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as f:
        f.write(audio.file.read())

    return file_path
