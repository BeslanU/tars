# TARS — Multi-Modal Summarization Engine

TARS (Text, Audio, and Resource Summarizer) is a smart, scalable app that transforms long-form content — including YouTube videos, articles, books, and audio files — into short, digestible summaries in both text and audio formats.

## 🚀 Features

- 🎥 **YouTube Summarization**: Paste a link and get a TL;DR, bullet points, or narrated summary.
- 📚 **Text & Book Summarization**: Upload or paste content to receive concise insights.
- 🔊 **Audio Transcription & Summarization**: Upload audio files and get summarized transcripts.
- 🗣️ **Text-to-Speech Output**: Listen to summaries via natural-sounding AI narration.
- 🧠 **Personal Digest Feed**: Save, tag, and organize summaries for later review.

## 🧱 Project Structure


## 🧪 Tech Stack

- **Frontend**: React Native / Next.js
- **Backend**: FastAPI / Node.js
- **AI/NLP**: OpenAI GPT, Whisper
- **TTS**: ElevenLabs / Google Cloud TTS
- **Storage/Auth**: Firebase / Supabase

## 🛠️ Setup

```bash
# Clone the repo
git clone https://github.com/BeslanU/tars.git
cd tars

# Install backend dependencies
cd server
pip install -r requirements.txt  # or npm install

# Start frontend
cd ../client
npm install
npm start
