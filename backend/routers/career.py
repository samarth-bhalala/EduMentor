"""
Career Planner Router - Skills analysis and roadmap generation
"""
from fastapi import APIRouter, HTTPException
from backend.models import SkillAnalyzeRequest, RoadmapRequest
from backend.database import get_db_connection
from backend.services.llm_service import analyze_skills_gap, generate_roadmap

router = APIRouter(prefix="/career", tags=["Career Planner"])

@router.post("/analyze")
async def analyze_skills(request: SkillAnalyzeRequest):
    """
    Analyze skill gaps for target role
    
    - Compares user skills vs predefined skill requirements
    - Identifies missing skills
    """
    try:
        missing_skills = analyze_skills_gap(request.user_skills, request.target_role)
        
        # Save user skills to database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Clear existing skills for user
        cursor.execute("DELETE FROM skills WHERE user_id = ?", (request.user_id,))
        
        # Add current skills
        for skill in request.user_skills:
            cursor.execute(
                "INSERT INTO skills (user_id, skill_name, proficiency_level) VALUES (?, ?, ?)",
                (request.user_id, skill, "intermediate")
            )
        
        conn.commit()
        conn.close()
        
        return {
            "user_skills": request.user_skills,
            "target_role": request.target_role,
            "missing_skills": missing_skills,
            "skill_match_percentage": round((len(request.user_skills) / 
                                            (len(request.user_skills) + len(missing_skills))) * 100, 2)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing skills: {str(e)}")

@router.post("/roadmap")
async def create_roadmap(request: RoadmapRequest):
    """
    Generate learning roadmap for career progression
    
    - Uses Hugging Face API to generate personalized roadmap
    - Stores in database
    """
    try:
        roadmap = generate_roadmap(request.target_role, request.missing_skills)
        
        # Save to database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO roadmaps (user_id, target_role, generated_plan) VALUES (?, ?, ?)",
            (request.user_id, request.target_role, roadmap)
        )
        conn.commit()
        roadmap_id = cursor.lastrowid
        conn.close()
        
        return {
            "roadmap_id": roadmap_id,
            "target_role": request.target_role,
            "roadmap": roadmap,
            "missing_skills": request.missing_skills
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating roadmap: {str(e)}")

@router.get("/roadmaps/{user_id}")
async def get_user_roadmaps(user_id: int):
    """Get all roadmaps for a user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM roadmaps WHERE user_id = ? ORDER BY created_at DESC",
        (user_id,)
    )
    roadmaps = cursor.fetchall()
    conn.close()
    
    return {
        "user_id": user_id,
        "roadmaps": [dict(roadmap) for roadmap in roadmaps]
    }

@router.get("/skills/{user_id}")
async def get_user_skills(user_id: int):
    """Get all skills for a user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT skill_name, proficiency_level FROM skills WHERE user_id = ?",
        (user_id,)
    )
    skills = cursor.fetchall()
    conn.close()
    
    return {
        "user_id": user_id,
        "skills": [{"name": s[0], "level": s[1]} for s in skills]
    }
