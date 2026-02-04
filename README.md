# Healthcare Doctor-Patient Translation Web Application

A real-time translation and communication platform for doctors and patients who speak different languages. This application bridges the language gap during medical consultations with AI-powered translation, audio recording, and intelligent summarization.

## Overview

During a doctor-patient consultation, language barriers can be a significant challenge. This application solves that by providing:

- **Real-time translation** between doctor and patient messages
- **Audio recording and transcription** for voice conversations
- **Conversation logging** with full history and timestamps
- **AI-powered summaries** that extract key medical information
- **Full-text search** across conversations
- **Multi-language support** for global accessibility

## Features

### Core Functionality

- **Doctor-Patient Chat Interface** - Clean, intuitive UI with role-based message distinction
- **Live Translation** - Automatic translation from source to target language using Google's Gemini AI
- **Audio Recording** - Direct browser-based audio recording with automatic transcription
- **Conversation History** - All messages persisted with timestamps, survives page refresh
- **Message Search** - Search across all messages with text highlighting
- **AI Summary** - Clinical summaries that extract symptoms, diagnoses, medications, and follow-up actions
- **Multi-Language Support** - English, Hindi, Spanish, and French

### Technical Features

- **Mobile-First Design** - Fully responsive on phones, tablets, and desktops
- **Real-time Updates** - Messages appear instantly after sending
- **Error Handling** - Graceful error messages and recovery
- **Fast Performance** - Optimized for quick load times and smooth interactions

## Tech Stack

### Frontend
- **React 18** - UI library
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Styling
- **Axios** - HTTP client
- **localStorage** - Client-side persistence

### Backend
- **FastAPI** - Web framework
- **SQLAlchemy** - Database ORM
- **Pydantic** - Data validation
- **Google Generative AI** - Translation and summarization
- **SQLite** - Database

### AI/LLM
- **Google Gemini 2.5 Flash** - Translation, summarization, and transcription

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js 16+
- Google Gemini API Key (free from [aistudio.google.com](https://aistudio.google.com/app/apikey))

### Installation

#### Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your API key
echo GEMINI_API_KEY=your-api-key-here > .env
```

#### Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create .env file (optional, defaults to localhost:8000)
echo VITE_API_URL=http://localhost:8000 > .env
```

### Running the Application

#### Terminal 1 - Backend
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python -m uvicorn app.main:app --reload --port 8000
```

The backend will start at `http://localhost:8000`

#### Terminal 2 - Frontend
```bash
cd frontend
npm run dev
```

The frontend will start at `http://localhost:5173`

#### Access the Application
Open your browser and navigate to `http://localhost:5173`

## Usage

### Basic Workflow

1. **Select Your Role** - Choose whether you're the Doctor or Patient
2. **Set Languages** - Select source language (your language) and target language (other person's language)
3. **Send Messages** - Type or speak your message
4. **View Translation** - See the message in the other language instantly
5. **Search History** - Use the search box to find previous messages
6. **Generate Summary** - Click the summary button to get a clinical overview

### Example Interaction

```
Doctor (English): "I see your symptoms suggest a viral infection"
↓ [Automatic Translation]
Patient (Hindi): "मुझे लगता है कि आपके लक्षण वायरल संक्रमण का सुझाव देते हैं"

Patient (Hindi): "मुझे तीन दिन से बुखार है"
↓ [Automatic Translation]
Doctor (English): "I have had a fever for three days"
```

## Project Structure

```
Healthcare_Convo/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── chat.py          # Message endpoints
│   │   │   ├── audio.py         # Audio upload & transcription
│   │   │   ├── search.py        # Search functionality
│   │   │   └── summary.py       # Summary generation
│   │   ├── models/
│   │   │   ├── message.py       # Message database model
│   │   │   └── conversation.py  # Conversation model
│   │   ├── services/
│   │   │   └── gemini_service.py # AI integration
│   │   ├── db/
│   │   │   ├── base.py
│   │   │   └── session.py
│   │   ├── schemas/
│   │   │   └── message_schema.py
│   │   └── main.py              # FastAPI app
│   ├── requirements.txt
│   └── .env                      # API keys (not in repo)
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatWindow.jsx       # Main chat interface
│   │   │   ├── MessageBubble.jsx    # Message display
│   │   │   ├── AudioRecorder.jsx    # Voice recording
│   │   │   ├── SearchBar.jsx        # Search interface
│   │   │   ├── SummaryPanel.jsx     # Summary display
│   │   │   ├── RoleSelector.jsx     # Role selection
│   │   │   └── LanguageSelector.jsx # Language selection
│   │   ├── pages/
│   │   │   └── ChatPage.jsx         # Main page
│   │   ├── services/
│   │   │   └── api.js               # API client
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
│
└── README.md
```

## API Endpoints

### Messages
- `POST /messages` - Send a text message
- `GET /messages/{conversation_id}` - Get all messages in a conversation

### Audio
- `POST /audio` - Upload and transcribe audio
- `GET /audio/{message_id}` - Get audio file info

### Search
- `GET /search?query=term` - Search all messages
- `GET /search/conversation/{conversation_id}` - Search specific conversation

### Summary
- `GET /summary?conversation_id=id&target_language=lang` - Generate conversation summary

### Health
- `GET /health` - API health check
- `GET /` - API information

## Features in Detail

### Real-time Translation
Messages are translated using Google's Gemini AI with medical terminology awareness. The system preserves medical meanings and accuracy.

### Audio Recording
Browser-based audio recording using the Web Audio API. Recorded audio is automatically transcribed and translated before being added to the conversation.

### Conversation Search
Full-text search across all messages. Matching text is highlighted in yellow. Search works across both original and translated text.

### AI Summaries
Summaries automatically extract:
- Chief complaint and symptoms
- Diagnoses
- Prescribed medications
- Follow-up actions and instructions
- Clinical observations

## Known Limitations

- Audio transcription quality depends on audio clarity
- Translation is performed by AI and may occasionally miss nuanced medical terminology
- Conversations are stored locally in SQLite (suitable for development, use PostgreSQL for production)
- Audio files are stored on disk (use S3 or cloud storage for production)

## Future Improvements

- [ ] Multiple conversation management
- [ ] Conversation export to PDF
- [ ] User authentication
- [ ] Cloud-based storage
- [ ] Real-time synchronization for multiple devices
- [ ] Specialist-specific medical context
- [ ] Prescription management
- [ ] Integration with EHR systems

## Production Deployment

### Environment Variables Required
```
GEMINI_API_KEY=your-api-key
DATABASE_URL=postgresql://user:password@host/db  # For production
```

### Recommended Changes for Production
- Use PostgreSQL instead of SQLite
- Add request rate limiting
- Enable HTTPS
- Add API authentication
- Use cloud storage for audio files
- Add comprehensive logging
- Set up monitoring and alerts
- Implement HIPAA compliance measures

### Deployment Options
- **Vercel** (Frontend) + **Render** (Backend)
- **AWS** (EC2, RDS, S3)
- **Google Cloud** (Cloud Run, Cloud SQL, Cloud Storage)
- **DigitalOcean** (App Platform)

## Testing

### Manual Testing Checklist
- [ ] Send text messages and verify translation
- [ ] Record audio and verify transcription
- [ ] Refresh page and verify message persistence
- [ ] Search for messages and verify highlighting
- [ ] Generate summary and verify medical info extraction
- [ ] Test with different language pairs
- [ ] Test on mobile device
- [ ] Test error scenarios (no internet, API errors)

## Troubleshooting

### Backend won't start
- Check Python version: `python --version` (need 3.8+)
- Verify API key is set in `.env`
- Check port 8000 isn't already in use

### Frontend won't start
- Check Node version: `node --version` (need 16+)
- Delete `node_modules` and run `npm install` again
- Clear browser cache

### Audio not recording
- Check browser microphone permission
- Try a different browser
- Check browser console for errors

### Translation seems wrong
- Check source and target languages are selected correctly
- API rate limits may cause delays, wait a moment and try again

## License

This project is created for educational purposes. Usage rights depend on your deployment and use case.

## Contact & Support

For issues or questions:
1. Check the troubleshooting section above
2. Review API documentation at `http://localhost:8000/docs`
3. Check browser console (F12) for error messages

## Acknowledgments

- Google Gemini API for translation and AI capabilities
- FastAPI for the excellent web framework
- React and Tailwind CSS for the frontend
- All open-source libraries used in this project

---

**Created:** February 2026  
**Status:** Active Development  
**Version:** 1.0.0
