"""
YouTube Summarizer Router - Extract and summarize YouTube videos
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.database import get_db_connection
from backend.services.llm_service import generate_text
from utils.youtube_parser import get_transcript, chunk_transcript
from datetime import datetime

router = APIRouter(prefix="/youtube", tags=["YouTube Summarizer"])

class YouTubeSummaryRequest(BaseModel):
    user_id: int
    video_url: str
    summary_type: str = "detailed"  # detailed, brief, bullet_points

@router.post("/summarize")
async def summarize_video(request: YouTubeSummaryRequest):
    """
    Summarize a YouTube video from its URL
    
    - Extracts transcript from YouTube video
    - Generates AI summary using LLM
    - Stores summary in database
    """
    try:
        # Get transcript
        transcript = get_transcript(request.video_url)
        
        if not transcript:
            raise HTTPException(status_code=400, detail="Could not extract transcript from video")
        
        # Chunk if too long (for very long videos)
        chunks = chunk_transcript(transcript, max_length=3000)
        
        # Generate summary based on type
        if request.summary_type == "brief":
            prompt = f"""Provide a brief 2-3 sentence summary of this YouTube video transcript:

{chunks[0][:2000]}

Brief Summary:"""
        elif request.summary_type == "bullet_points":
            prompt = f"""Create a bullet-point summary of the key points from this YouTube video transcript:

{chunks[0][:2000]}

Key Points:"""
        else:  # detailed
            prompt = f"""Provide a detailed summary of this YouTube video transcript. Include:
- Main topic and purpose
- Key points discussed
- Important takeaways

Transcript:
{chunks[0][:2000]}

Detailed Summary:"""
        
        # Generate summary using LLM
        summary = generate_text(prompt)
        
        # Save to database (create a summaries table entry)
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Create summaries table if not exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS youtube_summaries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                video_url TEXT NOT NULL,
                summary TEXT NOT NULL,
                summary_type TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        
        cursor.execute(
            "INSERT INTO youtube_summaries (user_id, video_url, summary, summary_type) VALUES (?, ?, ?, ?)",
            (request.user_id, request.video_url, summary, request.summary_type)
        )
        conn.commit()
        summary_id = cursor.lastrowid
        conn.close()
        
        return {
            "summary_id": summary_id,
            "video_url": request.video_url,
            "summary": summary,
            "summary_type": request.summary_type,
            "transcript_length": len(transcript),
            "word_count": len(transcript.split())
        }
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing video: {str(e)}")

@router.get("/summaries/{user_id}")
async def get_user_summaries(user_id: int):
    """Get all YouTube summaries for a user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Make sure table exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS youtube_summaries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            video_url TEXT NOT NULL,
            summary TEXT NOT NULL,
            summary_type TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    
    cursor.execute(
        "SELECT * FROM youtube_summaries WHERE user_id = ? ORDER BY created_at DESC",
        (user_id,)
    )
    summaries = cursor.fetchall()
    conn.close()
    
    return {
        "user_id": user_id,
        "summaries": [dict(summary) for summary in summaries]
    }
