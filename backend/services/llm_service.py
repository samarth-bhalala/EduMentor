"""
LLM Service using Hugging Face Inference API
"""
import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from typing import List, Dict

# Load environment variables from .env file
load_dotenv()

# Initialize Hugging Face client
# For hackathon: You can use free tier or set HF_TOKEN environment variable
HF_TOKEN = os.getenv("HF_TOKEN", None)
client = InferenceClient(token=HF_TOKEN)

print(f"🔑 HF Token loaded: {'Yes' if HF_TOKEN else 'No (using free tier)'}")

# Use a model that's well-supported for conversational/chat tasks
MODEL_NAME = "meta-llama/Meta-Llama-3-8B-Instruct"  # Alternative: "mistralai/Mixtral-8x7B-Instruct-v0.1"

def generate_text(prompt: str) -> str:
    """
    Generate text using Hugging Face Inference API with chat completion
    
    Args:
        prompt: Input text prompt
        
    Returns:
        Generated text response
    """
    try:
        messages = [{"role": "user", "content": prompt}]
        response = client.chat_completion(
            messages=messages,
            model=MODEL_NAME,
            max_tokens=500,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        error_msg = f"Hugging Face API Error: {str(e)}"
        print(f"❌ {error_msg}")
        return f"Error: Unable to generate response. {error_msg}"

def generate_answer(context: str, question: str) -> str:
    """
    Generate answer using retrieved context and question
    """
    prompt = f"""You are a helpful study assistant. Answer the question based on the provided context.

Context:
{context}

Question: {question}

Answer: """
    
    try:
        messages = [{"role": "user", "content": prompt}]
        response = client.chat_completion(
            messages=messages,
            model=MODEL_NAME,
            max_tokens=300,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating answer: {str(e)}. Please check your Hugging Face API setup."

def generate_quiz(topic: str, num_questions: int = 5) -> List[Dict]:
    """
    Generate MCQ quiz questions on a given topic
    """
    prompt = f"""Generate {num_questions} multiple choice questions about {topic}.

Format each question exactly as:
Q: [question text]
A) [option 1]
B) [option 2]
C) [option 3]
D) [option 4]
Correct: [A/B/C/D]

Generate the questions now:"""

    try:
        messages = [{"role": "user", "content": prompt}]
        response = client.chat_completion(
            messages=messages,
            model=MODEL_NAME,
            max_tokens=800,
            temperature=0.8
        )
        
        # Parse response into structured format
        questions = parse_quiz_response(response.choices[0].message.content, num_questions)
        return questions
    except Exception as e:
        # Return sample questions as fallback
        return generate_sample_quiz(topic, num_questions)

def parse_quiz_response(response: str, num_questions: int) -> List[Dict]:
    """Parse LLM response into structured quiz format"""
    questions = []
    lines = response.split('\n')
    current_q = {}
    options = []
    
    for line in lines:
        line = line.strip()
        if line.startswith('Q:'):
            if current_q and options:
                current_q['options'] = options
                questions.append(current_q)
            current_q = {'question': line[2:].strip()}
            options = []
        elif line.startswith(('A)', 'B)', 'C)', 'D)')):
            options.append(line[2:].strip())
        elif line.startswith('Correct:'):
            answer = line.split(':')[1].strip().upper()
            answer_map = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
            current_q['correct_answer'] = answer_map.get(answer, 0)
    
    if current_q and options:
        current_q['options'] = options
        questions.append(current_q)
    
    # Ensure we have the right number of questions
    while len(questions) < num_questions:
        questions.append(generate_sample_question(len(questions) + 1))
    
    return questions[:num_questions]

def generate_sample_question(index: int) -> Dict:
    """Generate a sample question as fallback"""
    return {
        'question': f'Sample question {index}',
        'options': ['Option A', 'Option B', 'Option C', 'Option D'],
        'correct_answer': 0
    }

def generate_sample_quiz(topic: str, num_questions: int) -> List[Dict]:
    """Generate sample quiz as fallback"""
    return [generate_sample_question(i+1) for i in range(num_questions)]

def generate_roadmap(target_role: str, missing_skills: List[str]) -> str:
    """
    Generate learning roadmap for career progression
    """
    skills_str = ", ".join(missing_skills)
    prompt = f"""Create a detailed 6-month learning roadmap for someone who wants to become a {target_role}.

They need to learn: {skills_str}

Provide a week-by-week plan with:
- Resources to study
- Projects to build
- Milestones to achieve

Roadmap:"""

    try:
        messages = [{"role": "user", "content": prompt}]
        response = client.chat_completion(
            messages=messages,
            model=MODEL_NAME,
            max_tokens=600,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating roadmap: {str(e)}. Please check your Hugging Face API setup."

def analyze_skills_gap(user_skills: List[str], target_role: str) -> List[str]:
    """
    Analyze gap between user skills and target role requirements
    """
    # Predefined skill requirements for common roles
    role_skills = {
        "Data Scientist": [
            "Python", "Machine Learning", "Statistics", "SQL", 
            "Deep Learning", "Data Visualization", "Pandas", "NumPy"
        ],
        "Full Stack Developer": [
            "JavaScript", "React", "Node.js", "Python", "SQL", 
            "REST APIs", "Git", "HTML/CSS"
        ],
        "DevOps Engineer": [
            "Docker", "Kubernetes", "CI/CD", "AWS", "Linux", 
            "Python", "Terraform", "Monitoring"
        ],
        "ML Engineer": [
            "Python", "TensorFlow", "PyTorch", "MLOps", "Docker", 
            "Cloud Platforms", "Model Deployment", "Data Engineering"
        ]
    }
    
    required_skills = role_skills.get(target_role, [])
    user_skills_lower = [s.lower() for s in user_skills]
    missing = [skill for skill in required_skills 
               if skill.lower() not in user_skills_lower]
    
    return missing
