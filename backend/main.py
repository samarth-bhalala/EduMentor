"""
FastAPI Backend for EduMentor AI
Main entry point for the API server
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.database import init_database
from backend.routers import study, quiz, career, youtube, doubt_solver

# Initialize FastAPI app
app = FastAPI(
    title="EduMentor AI API",
    description="AI-powered educational platform with RAG, Quiz, and Career Planning",
    version="1.0.0"
)

# CORS middleware for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_database()
    print("🚀 EduMentor AI Backend is ready!")

# Include routers
app.include_router(study.router)
app.include_router(quiz.router)
app.include_router(career.router)
app.include_router(youtube.router)
app.include_router(doubt_solver.router)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to EduMentor AI API",
        "version": "1.0.0",
        "endpoints": {
            "study": "/study",
            "quiz": "/quiz",
            "career": "/career",
            "youtube": "/youtube",
            "doubt-solver": "/doubt-solver"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
