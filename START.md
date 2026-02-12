# 🚀 EduMentor AI - Quick Start Guide

## ✅ Setup Complete!

All files have been created and the backend is ready to run.

## 📦 Installation

```powershell
# Install dependencies
python -m pip install fastapi uvicorn[standard] python-multipart sqlalchemy streamlit plotly requests sentence-transformers faiss-cpu huggingface-hub PyPDF2 python-dotenv pydantic[email]
```

## 🏃 Running the Application

### Terminal 1: Start Backend (FastAPI)

```powershell
cd a:\Projects\hackathon
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

✅ Backend will be available at: **http://localhost:8000**
✅ API Documentation: **http://localhost:8000/docs**

### Terminal 2: Start Frontend (Streamlit)

```powershell
cd a:\Projects\hackathon
streamlit run app.py
```

✅ Frontend will open automatically at: **http://localhost:8501**

## 🎯 Features to Demo

### 1. Study Buddy (RAG System)
- Upload a PDF document
- Ask questions about the content
- Get AI-powered answers with context

### 2. Quiz Generator
- Enter a topic (e.g., "Python Programming")
- Generate 5 MCQ questions
- Take the quiz and see your score

### 3. Career Planner
- Select target role (Data Scientist, Full Stack Developer, etc.)
- Enter your current skills
- Analyze skill gaps
- Generate personalized learning roadmap

### 4. Analytics Dashboard
- View quiz performance over time
- Track learning progress
- Performance insights by topic

## 📁 Project Structure

```
✅ backend/main.py - FastAPI server
✅ backend/database.py - SQLite database
✅ backend/services/llm_service.py - Hugging Face integration
✅ backend/services/rag_service.py - FAISS vector search
✅ backend/routers/study.py - Study Buddy endpoints
✅ backend/routers/quiz.py - Quiz endpoints
✅ backend/routers/career.py - Career Planner endpoints
✅ utils/pdf_parser.py - PDF processing
✅ utils/embeddings.py - Embedding generation
✅ app.py - Streamlit frontend
```

## 🔧 Optional: Hugging Face Token

For better API rate limits, set your Hugging Face token:

1. Get token from: https://huggingface.co/settings/tokens
2. Create `.env` file:
```bash
HF_TOKEN=your_token_here
```

The app works without a token using the free tier!

## 🎓 Tech Stack

- Backend: FastAPI
- Frontend: Streamlit
- Database: SQLite
- Vector DB: FAISS
- Embeddings: sentence-transformers (all-MiniLM-L6-v2)
- LLM: Mistral-7B-Instruct-v0.2 (Hugging Face)

## 🚀 You're All Set!

Your hackathon project is ready to demo! 🎉
