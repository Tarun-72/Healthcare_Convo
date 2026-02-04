import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")

def translate_text(text: str, source_lang: str, target_lang: str) -> str:
    """
    Translate medical text from source language to target language.
    Preserves medical terminology and meaning.
    """
    if not text or not text.strip():
        return ""
    
    if source_lang == target_lang:
        return text
    
    try:
        prompt = f"""You are a professional medical translator.
Translate the following medical message from {source_lang} to {target_lang}.
Preserve all medical terminology and meaning accurately.
Only return the translated text, nothing else.

Message to translate:
"{text}"
"""
        response = model.generate_content(prompt, safety_settings=[
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE"
            }
        ])
        
        translated = response.text.strip()
        if not translated:
            return text  # Return original if translation fails
        return translated
        
    except Exception as e:
        print(f"Translation error: {str(e)}")
        return text  # Fallback to original text

def summarize_conversation(conversation_text: str, target_language: str = "English") -> str:
    """
    Generate a clinical summary of a doctor-patient conversation.
    Highlights medical important points and follow-up actions.
    Returns summary in the target language.
    """
    if not conversation_text or not conversation_text.strip():
        return "No conversation content to summarize."
    
    try:
        language_instruction = f"Provide the summary in {target_language}." if target_language != "English" else ""
        
        prompt = f"""You are a clinical documentation specialist.
Analyze this doctor-patient conversation and create a concise medical summary.

Extract and highlight:
1. CHIEF COMPLAINT / SYMPTOMS - What the patient reported
2. DIAGNOSES - What the doctor diagnosed (if any)
3. MEDICATIONS - Any medications prescribed or discussed
4. FOLLOW-UP ACTIONS - What needs to happen next
5. CLINICAL NOTES - Any important medical observations

Format the summary clearly with these sections.
{language_instruction}

Conversation:
{conversation_text}

Summary:"""
        
        response = model.generate_content(prompt, safety_settings=[
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE"
            }
        ])
        
        summary = response.text.strip()
        if not summary:
            return "Unable to generate summary at this time."
        return summary
        
    except Exception as e:
        print(f"Summary generation error: {str(e)}")
        return f"Error generating summary: {str(e)}"

def transcribe_audio(audio_path: str) -> str:
    """
    Transcribe audio file to text using Gemini API.
    Note: For production, consider using Google Cloud Speech-to-Text API
    """
    try:
        # Upload the file to Gemini (supports audio transcription)
        audio_file = genai.upload_file(audio_path)
        
        prompt = "Please transcribe this medical conversation audio to text. Preserve all medical terminology accurately."
        
        response = model.generate_content([audio_file, prompt])
        
        transcribed = response.text.strip()
        return transcribed if transcribed else ""
        
    except Exception as e:
        print(f"Transcription error: {str(e)}")
        return ""

