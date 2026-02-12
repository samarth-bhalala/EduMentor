"""
Study Buddy Router - RAG-based Q&A system
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.models import QuestionRequest
from backend.database import get_db_connection
from backend.services.rag_service import rag_service
from backend.services.llm_service import generate_answer
from utils.pdf_parser import process_pdf
import os
import shutil
from datetime import datetime

router = APIRouter(prefix="/study", tags=["Study Buddy"])

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_document(user_id: int, file: UploadFile = File(...)):
    """
    Upload and process a PDF document
    
    - Extracts text from PDF
    - Chunks into 500-word segments
    - Generates embeddings
    - Stores in FAISS
    - Saves metadata to SQLite
    """
    # Validate file type
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    try:
        # Save uploaded file
        file_path = os.path.join(UPLOAD_DIR, f"{user_id}_{file.filename}")
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Process PDF: extract text and chunk
        chunks = process_pdf(file_path, chunk_size=500)
        
        if not chunks:
            raise HTTPException(status_code=400, detail="No text could be extracted from PDF")
        
        # Add to RAG service
        metadata = {
            'user_id': user_id,
            'file_name': file.filename,
            'upload_time': datetime.now().isoformat()
        }
        rag_service.add_documents(chunks, metadata)
        
        # Save to database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO documents (user_id, file_name) VALUES (?, ?)",
            (user_id, file.filename)
        )
        conn.commit()
        doc_id = cursor.lastrowid
        conn.close()
        
        return {
            "status": "success",
            "message": f"Processed {len(chunks)} chunks from {file.filename}",
            "document_id": doc_id,
            "chunks_count": len(chunks)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@router.post("/ask")
async def ask_question(request: QuestionRequest):
    """
    Ask a question using RAG system
    
    - Embeds the question
    - Retrieves top 3 similar chunks from FAISS
    - Sends context + question to Hugging Face API
    - Returns generated answer
    """
    try:
        # Retrieve relevant context
        context = rag_service.get_context(request.question, top_k=3)
        
        # Generate answer using LLM
        answer = generate_answer(context, request.question)
        
        return {
            "question": request.question,
            "answer": answer,
            "context_used": context[:500] + "..." if len(context) > 500 else context
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating answer: {str(e)}")

@router.get("/documents/{user_id}")
async def get_user_documents(user_id: int):
    """Get all documents uploaded by a user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM documents WHERE user_id = ? ORDER BY upload_time DESC",
        (user_id,)
    )
    docs = cursor.fetchall()
    conn.close()
    
    return {
        "user_id": user_id,
        "documents": [dict(doc) for doc in docs]
    }
