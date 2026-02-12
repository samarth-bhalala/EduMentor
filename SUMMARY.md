# EduMentor AI - Project Summary

## 🎯 Overview
**EduMentor AI** is a comprehensive AI-powered educational platform built for hackathons. It combines multiple AI features including RAG (Retrieval-Augmented Generation), quiz generation, career planning, YouTube summarization, and a smart chatbot tutor.

## ✨ Features Implemented

### 1. 📚 Study Buddy (RAG System)
**Models Used:**
- **Embedding Model**: `sentence-transformers/all-MiniLM-L6-v2` (384 dimensions)
- **LLM**: `Meta-Llama-3-8B-Instruct` (via Hugging Face Inference API)
- **Vector DB**: FAISS IndexFlatL2

**Features:**
- Upload PDF documents and extract text content
- Create vector embeddings for semantic search
- Store embeddings in FAISS vector database
- Ask questions and get AI-powered answers based on your documents
- Context-aware responses using RAG architecture

### 2. 💬 Smart Doubt Solver Chatbot
**Models Used:**
- **LLM**: `Meta-Llama-3-8B-Instruct` (via Hugging Face Inference API)

**Features:**
- Interactive AI tutor with conversation history
- Context-aware responses that remember previous messages
- Step-by-step explanations for complex topics
- Persistent chat history stored in SQLite database
- Clear chat history option

### 3. 🎥 YouTube Summarizer
**Models Used:**
- **LLM**: `Meta-Llama-3-8B-Instruct` (via Hugging Face Inference API)

**Features:**
- Extract transcripts from YouTube videos using youtube-transcript-api
- Generate AI summaries (detailed, brief, or bullet points)
- Save summary history for each user
- Video embedding and metadata display

### 4. ❓ Quiz Generator
**Models Used:**
- **LLM**: `Meta-Llama-3-8B-Instruct` (via Hugging Face Inference API)

**Features:**
- Generate AI-powered multiple-choice questions on any topic
- Automatic grading and scoring
- Save quiz results to database
- Track performance over time

### 5. 🚀 Career Planner
**Models Used:**
- **LLM**: `Meta-Llama-3-8B-Instruct` (via Hugging Face Inference API)

**Features:**
- Analyze user skills against target job roles
- Identify skill gaps
- Generate personalized learning roadmaps
- AI-powered career guidance

### 6. 📊 Analytics Dashboard
**Models Used:**
- **Visualization**: Plotly (no AI models, pure data visualization)

**Features:**
- Visualize quiz performance with charts
- Track learning progress
- Display user statistics
- Interactive Plotly graphs

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLite** - Lightweight database with 6 tables (users, documents, quiz_results, skills, roadmaps, chat_history, youtube_summaries)
- **FAISS** - Facebook's vector similarity search library
- **sentence-transformers** - Text embedding models (384 dimensions)
- **Hugging Face Inference API** - LLM integration (Meta-Llama-3-8B-Instruct)
- **PyPDF2** - PDF text extraction
- **youtube-transcript-api** - YouTube transcript fetching

### Frontend
- **Streamlit** - Interactive web UI with 7 pages
- **Plotly** - Data visualization
- **Requests** - API communication

### AI/ML
- **Vector Embeddings**: all-MiniLM-L6-v2 model
- **Vector Database**: FAISS IndexFlatL2
- **LLM**: Meta-Llama-3-8B-Instruct via Hugging Face
- **RAG**: Custom implementation with semantic search

## 📁 Project Structure

```
hackathon/
├── backend/
│   ├── main.py                    # FastAPI app entry point
│   ├── database.py                # SQLite connection & tables
│   ├── models.py                  # Pydantic request/response models
│   ├── routers/
│   │   ├── study.py              # PDF upload & Q&A endpoints
│   │   ├── quiz.py               # Quiz generation & grading
│   │   ├── career.py             # Skills analysis & roadmap
│   │   ├── youtube.py            # Video summarization
│   │   └── doubt_solver.py       # Chatbot endpoints
│   └── services/
│       ├── llm_service.py        # Hugging Face API client
│       └── rag_service.py        # FAISS vector search
├── utils/
│   ├── pdf_parser.py             # PDF text extraction
│   ├── embeddings.py             # Text embedding generation
│   └── youtube_parser.py         # YouTube transcript extraction
├── app.py                         # Streamlit frontend
├── requirements.txt               # Python dependencies
├── .env                          # Environment variables (HF_TOKEN)
└── data/
    ├── db.sqlite                 # SQLite database
    └── faiss_index/              # Vector index storage
```

## 🚀 How to Run

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Hugging Face Token**
   - Create `.env` file
   - Add: `HF_TOKEN=your_token_here`

3. **Start Backend**
   ```bash
   python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
   ```

4. **Start Frontend**
   ```bash
   python -m streamlit run app.py
   ```

5. **Access Application**
   - Frontend: http://localhost:8502
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## 🎓 Key Technical Highlights

1. **RAG Implementation**: Custom vector search with FAISS for document Q&A
2. **Context-Aware Chatbot**: Maintains conversation history for better responses
3. **Multi-Modal AI**: Text generation, summarization, quiz creation, and analysis
4. **Real-Time Processing**: Async FastAPI endpoints with streaming support
5. **Persistent Storage**: SQLite for all user data and conversation history
6. **Modular Architecture**: Clean separation of routers, services, and utilities

## 📊 Database Schema

- **users**: User profiles (id, name, email, goal)
- **documents**: Uploaded PDFs (id, user_id, file_name, upload_time)
- **quiz_results**: Quiz scores (id, user_id, topic, score, total, timestamp)
- **skills**: User skills (id, user_id, skill_name, proficiency_level)
- **roadmaps**: Career plans (id, user_id, target_role, generated_plan)
- **chat_history**: Chatbot conversations (id, user_id, message, is_user, timestamp)
- **youtube_summaries**: Video summaries (id, user_id, video_url, summary, summary_type)

## 💡 What Makes This Project Special

- **All-in-One Platform**: Combines 6 different AI features in one application
- **Production-Ready**: Proper error handling, database management, and API structure
- **Scalable Architecture**: Modular design allows easy addition of new features
- **Educational Focus**: Designed specifically for learning and skill development
- **Hackathon-Ready**: Fast setup, comprehensive features, impressive demo potential

## 🔧 Environment Variables

- `HF_TOKEN`: Hugging Face API token for LLM access

## 📈 Future Enhancements (Ideas)

- User authentication and authorization
- File upload support for more formats (DOCX, TXT, etc.)
- Voice-to-text for chatbot interactions
- Collaborative study rooms
- Spaced repetition quiz system
- Progress tracking and gamification
- Export study notes and summaries

---

**Built with ❤️ using FastAPI, Streamlit, and Hugging Face**
