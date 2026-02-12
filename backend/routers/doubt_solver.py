"""
Smart Doubt Solver Chatbot Router
"""
from fastapi import APIRouter, HTTPException
from backend.models import ChatMessage, ChatHistoryResponse
from backend.database import get_db_connection
from backend.services.llm_service import generate_text
from typing import List
from datetime import datetime

router = APIRouter(prefix="/doubt-solver", tags=["Doubt Solver"])

@router.post("/chat")
async def send_message(request: ChatMessage):
    """
    Send a message to the doubt solver chatbot
    
    Args:
        request: ChatMessage with user_id and message
        
    Returns:
        AI response and confirmation
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Save user message to database
        cursor.execute(
            "INSERT INTO chat_history (user_id, message, is_user) VALUES (?, ?, ?)",
            (request.user_id, request.message, True)
        )
        
        # Get chat history for context (last 10 messages)
        cursor.execute(
            """SELECT message, is_user FROM chat_history 
               WHERE user_id = ? 
               ORDER BY timestamp DESC 
               LIMIT 10""",
            (request.user_id,)
        )
        history = cursor.fetchall()
        history.reverse()  # Chronological order
        
        # Build conversation context
        conversation = []
        for msg in history[:-1]:  # Exclude the current message
            role = "Student" if msg[1] else "AI Tutor"
            conversation.append(f"{role}: {msg[0]}")
        
        context = "\n".join(conversation) if conversation else "Start of conversation"
        
        # Generate AI response with context
        prompt = f"""You are an expert AI tutor helping students solve their doubts. Be clear, patient, and educational.

Previous conversation:
{context}

Student's current question: {request.message}

Provide a helpful, detailed explanation. If it's a concept, explain it clearly. If it's a problem, guide them through the solution step by step."""
        
        ai_response = generate_text(prompt)
        
        # Save AI response to database
        cursor.execute(
            "INSERT INTO chat_history (user_id, message, is_user) VALUES (?, ?, ?)",
            (request.user_id, ai_response, False)
        )
        
        conn.commit()
        conn.close()
        
        return {
            "success": True,
            "user_message": request.message,
            "ai_response": ai_response
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")

@router.get("/history/{user_id}", response_model=List[ChatHistoryResponse])
async def get_chat_history(user_id: int):
    """
    Get chat history for a user
    
    Args:
        user_id: User ID
        
    Returns:
        List of chat messages
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """SELECT id, message, is_user, timestamp 
               FROM chat_history 
               WHERE user_id = ? 
               ORDER BY timestamp ASC""",
            (user_id,)
        )
        
        messages = cursor.fetchall()
        conn.close()
        
        return [
            {
                "id": msg[0],
                "message": msg[1],
                "is_user": bool(msg[2]),
                "timestamp": msg[3]
            }
            for msg in messages
        ]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching chat history: {str(e)}")

@router.delete("/history/{user_id}")
async def clear_chat_history(user_id: int):
    """
    Clear chat history for a user
    
    Args:
        user_id: User ID
        
    Returns:
        Confirmation message
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM chat_history WHERE user_id = ?", (user_id,))
        
        conn.commit()
        conn.close()
        
        return {"success": True, "message": "Chat history cleared"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing chat history: {str(e)}")
