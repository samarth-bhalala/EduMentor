"""
Quiz Router - AI-generated quiz system
"""
from fastapi import APIRouter, HTTPException
from backend.models import QuizGenerateRequest, QuizSubmitRequest
from backend.database import get_db_connection
from backend.services.llm_service import generate_quiz

router = APIRouter(prefix="/quiz", tags=["Quiz"])

@router.post("/generate")
async def generate_quiz_endpoint(request: QuizGenerateRequest):
    """
    Generate MCQ quiz on a given topic
    
    - Uses Hugging Face API to generate questions
    - Returns JSON format with questions, options, and correct answers
    """
    try:
        questions = generate_quiz(request.topic, request.num_questions)
        
        return {
            "topic": request.topic,
            "num_questions": len(questions),
            "questions": questions
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating quiz: {str(e)}")

@router.post("/submit")
async def submit_quiz(request: QuizSubmitRequest):
    """
    Submit quiz answers and calculate score
    
    - Compares user answers with correct answers
    - Calculates score
    - Stores result in SQLite
    """
    try:
        # Calculate score
        score = sum(1 for user_ans, correct_ans in zip(request.answers, request.correct_answers) 
                   if user_ans == correct_ans)
        total = len(request.correct_answers)
        percentage = (score / total * 100) if total > 0 else 0
        
        # Save to database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO quiz_results (user_id, topic, score, total) VALUES (?, ?, ?, ?)",
            (request.user_id, request.topic, score, total)
        )
        conn.commit()
        result_id = cursor.lastrowid
        conn.close()
        
        return {
            "result_id": result_id,
            "score": score,
            "total": total,
            "percentage": round(percentage, 2),
            "passed": percentage >= 70
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error submitting quiz: {str(e)}")

@router.get("/results/{user_id}")
async def get_quiz_results(user_id: int):
    """Get all quiz results for a user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM quiz_results WHERE user_id = ? ORDER BY timestamp DESC",
        (user_id,)
    )
    results = cursor.fetchall()
    conn.close()
    
    return {
        "user_id": user_id,
        "results": [dict(result) for result in results]
    }
