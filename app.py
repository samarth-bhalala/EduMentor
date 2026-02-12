"""
EduMentor AI - Streamlit Frontend
Main application interface
"""
import streamlit as st
import requests
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# Configuration
API_BASE_URL = "http://localhost:8000"

# Page configuration
st.set_page_config(
    page_title="EduMentor AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'user_id' not in st.session_state:
    st.session_state.user_id = 1  # Default user for hackathon demo

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
        padding: 1rem 0;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #424242;
        text-align: center;
        margin-bottom: 2rem;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #E8F5E9;
        border-left: 5px solid #4CAF50;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #E3F2FD;
        border-left: 5px solid #2196F3;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("🎓 EduMentor AI")
st.sidebar.markdown("---")
page = st.sidebar.radio(
    "Navigate",
    ["🏠 Home", "📚 Study Buddy", "❓ Quiz", "🚀 Career Planner", "📊 Analytics"]
)
st.sidebar.markdown("---")
st.sidebar.info(f"**User ID:** {st.session_state.user_id}")

# ==================== HOME PAGE ====================
if page == "🏠 Home":
    st.markdown('<div class="main-header">🎓 EduMentor AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Your AI-Powered Learning Companion</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📚 Study Buddy")
        st.write("Upload PDFs and ask questions using AI-powered RAG system")
        st.info("✨ Context-aware answers from your documents")
    
    with col2:
        st.markdown("### ❓ Quiz Generator")
        st.write("Generate AI quizzes on any topic and test your knowledge")
        st.info("✨ Instant feedback and progress tracking")
    
    with col3:
        st.markdown("### 🚀 Career Planner")
        st.write("Analyze skills and get personalized learning roadmaps")
        st.info("✨ AI-generated career guidance")
    
    st.markdown("---")
    st.markdown("### 🎯 Features")
    features = [
        "📄 PDF document processing with intelligent chunking",
        "🧠 Vector similarity search using FAISS",
        "💬 Conversational AI powered by Mistral-7B",
        "📝 Automated quiz generation and grading",
        "📈 Skills gap analysis",
        "🗺️ Personalized learning roadmaps",
        "📊 Progress analytics and visualization"
    ]
    for feature in features:
        st.markdown(f"- {feature}")

# ==================== STUDY BUDDY PAGE ====================
elif page == "📚 Study Buddy":
    st.title("📚 Study Buddy - RAG System")
    st.markdown("Upload PDFs and ask questions to get AI-powered answers based on your documents.")
    
    tab1, tab2 = st.tabs(["📤 Upload Document", "💬 Ask Questions"])
    
    with tab1:
        st.subheader("Upload PDF Document")
        uploaded_file = st.file_uploader("Choose a PDF file", type=['pdf'])
        
        if uploaded_file:
            if st.button("🚀 Process Document", type="primary"):
                with st.spinner("Processing PDF... This may take a moment."):
                    try:
                        files = {'file': (uploaded_file.name, uploaded_file, 'application/pdf')}
                        response = requests.post(
                            f"{API_BASE_URL}/study/upload",
                            params={'user_id': st.session_state.user_id},
                            files=files
                        )
                        
                        if response.status_code == 200:
                            result = response.json()
                            st.success(f"✅ {result['message']}")
                            st.info(f"📊 Processed {result['chunks_count']} text chunks")
                        else:
                            st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
                    except Exception as e:
                        st.error(f"Connection error: {str(e)}\n\nMake sure the backend is running on port 8000")
        
        # Show uploaded documents
        st.markdown("---")
        st.subheader("📁 My Documents")
        try:
            response = requests.get(f"{API_BASE_URL}/study/documents/{st.session_state.user_id}")
            if response.status_code == 200:
                docs = response.json()['documents']
                if docs:
                    for doc in docs:
                        st.markdown(f"- **{doc['file_name']}** (uploaded: {doc['upload_time']})")
                else:
                    st.info("No documents uploaded yet")
        except:
            st.warning("Could not load documents. Make sure backend is running.")
    
    with tab2:
        st.subheader("Ask a Question")
        question = st.text_area("Enter your question:", placeholder="What is the main concept discussed in the document?")
        
        if st.button("🔍 Get Answer", type="primary"):
            if question:
                with st.spinner("Generating answer..."):
                    try:
                        response = requests.post(
                            f"{API_BASE_URL}/study/ask",
                            json={
                                'user_id': st.session_state.user_id,
                                'question': question
                            }
                        )
                        
                        if response.status_code == 200:
                            result = response.json()
                            st.markdown("### 💡 Answer:")
                            st.success(result['answer'])
                            
                            with st.expander("📄 View Context Used"):
                                st.text(result['context_used'])
                        else:
                            st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
                    except Exception as e:
                        st.error(f"Connection error: {str(e)}")
            else:
                st.warning("Please enter a question")

# ==================== QUIZ PAGE ====================
elif page == "❓ Quiz":
    st.title("❓ Quiz Generator")
    st.markdown("Generate AI-powered quizzes on any topic and test your knowledge!")
    
    tab1, tab2 = st.tabs(["📝 Take Quiz", "📊 Results"])
    
    with tab1:
        st.subheader("Generate New Quiz")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            topic = st.text_input("Quiz Topic:", placeholder="e.g., Python Programming, Machine Learning, etc.")
        with col2:
            num_questions = st.number_input("Number of Questions:", min_value=3, max_value=10, value=5)
        
        if st.button("🎯 Generate Quiz", type="primary"):
            if topic:
                with st.spinner("Generating quiz questions..."):
                    try:
                        response = requests.post(
                            f"{API_BASE_URL}/quiz/generate",
                            json={
                                'user_id': st.session_state.user_id,
                                'topic': topic,
                                'num_questions': num_questions
                            }
                        )
                        
                        if response.status_code == 200:
                            st.session_state.quiz_data = response.json()
                            st.session_state.quiz_topic = topic
                            st.success("✅ Quiz generated successfully!")
                        else:
                            st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
                    except Exception as e:
                        st.error(f"Connection error: {str(e)}")
            else:
                st.warning("Please enter a topic")
        
        # Display quiz if generated
        if 'quiz_data' in st.session_state:
            st.markdown("---")
            st.markdown(f"### 📝 Quiz: {st.session_state.quiz_topic}")
            
            user_answers = []
            correct_answers = []
            
            for i, q in enumerate(st.session_state.quiz_data['questions']):
                st.markdown(f"**Question {i+1}:** {q['question']}")
                answer = st.radio(
                    f"Select answer for Q{i+1}:",
                    options=range(len(q['options'])),
                    format_func=lambda x, opts=q['options']: f"{chr(65+x)}) {opts[x]}",
                    key=f"q_{i}"
                )
                user_answers.append(answer)
                correct_answers.append(q['correct_answer'])
                st.markdown("---")
            
            if st.button("✅ Submit Quiz", type="primary"):
                with st.spinner("Calculating score..."):
                    try:
                        response = requests.post(
                            f"{API_BASE_URL}/quiz/submit",
                            json={
                                'user_id': st.session_state.user_id,
                                'topic': st.session_state.quiz_topic,
                                'answers': user_answers,
                                'correct_answers': correct_answers
                            }
                        )
                        
                        if response.status_code == 200:
                            result = response.json()
                            
                            # Display results
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Score", f"{result['score']}/{result['total']}")
                            with col2:
                                st.metric("Percentage", f"{result['percentage']}%")
                            with col3:
                                status = "✅ PASSED" if result['passed'] else "❌ FAILED"
                                st.metric("Status", status)
                            
                            # Clear quiz data
                            del st.session_state.quiz_data
                            st.balloons()
                        else:
                            st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
                    except Exception as e:
                        st.error(f"Connection error: {str(e)}")
    
    with tab2:
        st.subheader("📊 Quiz History")
        try:
            response = requests.get(f"{API_BASE_URL}/quiz/results/{st.session_state.user_id}")
            if response.status_code == 200:
                results = response.json()['results']
                
                if results:
                    for result in results:
                        percentage = (result['score'] / result['total'] * 100)
                        status = "✅" if percentage >= 70 else "❌"
                        st.markdown(f"{status} **{result['topic']}** - {result['score']}/{result['total']} ({percentage:.0f}%) - {result['timestamp']}")
                else:
                    st.info("No quiz results yet. Take a quiz to see your results here!")
        except:
            st.warning("Could not load results. Make sure backend is running.")

# ==================== CAREER PLANNER PAGE ====================
elif page == "🚀 Career Planner":
    st.title("🚀 Career Planner")
    st.markdown("Analyze your skills and get personalized learning roadmaps for your dream role!")
    
    tab1, tab2 = st.tabs(["🎯 Skills Analysis", "🗺️ Learning Roadmap"])
    
    with tab1:
        st.subheader("Skills Gap Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            target_role = st.selectbox(
                "Target Role:",
                ["Data Scientist", "Full Stack Developer", "DevOps Engineer", "ML Engineer"]
            )
        
        with col2:
            st.markdown("**Your Skills:**")
            skills_input = st.text_area(
                "Enter your skills (comma-separated):",
                placeholder="Python, SQL, Machine Learning, etc.",
                height=100
            )
        
        if st.button("🔍 Analyze Skills", type="primary"):
            if skills_input:
                user_skills = [s.strip() for s in skills_input.split(',')]
                
                with st.spinner("Analyzing skills..."):
                    try:
                        response = requests.post(
                            f"{API_BASE_URL}/career/analyze",
                            json={
                                'user_id': st.session_state.user_id,
                                'user_skills': user_skills,
                                'target_role': target_role
                            }
                        )
                        
                        if response.status_code == 200:
                            result = response.json()
                            st.session_state.analysis_result = result
                            
                            # Display results
                            st.markdown("### 📊 Analysis Results")
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                st.metric("Skill Match", f"{result['skill_match_percentage']}%")
                            with col2:
                                st.metric("Missing Skills", len(result['missing_skills']))
                            
                            st.markdown("---")
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown("#### ✅ Your Skills")
                                for skill in result['user_skills']:
                                    st.markdown(f"- {skill}")
                            
                            with col2:
                                st.markdown("#### ❌ Missing Skills")
                                if result['missing_skills']:
                                    for skill in result['missing_skills']:
                                        st.markdown(f"- {skill}")
                                else:
                                    st.success("No missing skills! You're ready! 🎉")
                        else:
                            st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
                    except Exception as e:
                        st.error(f"Connection error: {str(e)}")
            else:
                st.warning("Please enter your skills")
    
    with tab2:
        st.subheader("🗺️ Generate Learning Roadmap")
        
        if 'analysis_result' in st.session_state:
            result = st.session_state.analysis_result
            
            st.info(f"**Target Role:** {result['target_role']}")
            st.warning(f"**Skills to Learn:** {', '.join(result['missing_skills']) if result['missing_skills'] else 'None'}")
            
            if st.button("🚀 Generate Roadmap", type="primary"):
                if result['missing_skills']:
                    with st.spinner("Generating personalized roadmap..."):
                        try:
                            response = requests.post(
                                f"{API_BASE_URL}/career/roadmap",
                                json={
                                    'user_id': st.session_state.user_id,
                                    'target_role': result['target_role'],
                                    'missing_skills': result['missing_skills']
                                }
                            )
                            
                            if response.status_code == 200:
                                roadmap = response.json()
                                
                                st.markdown("### 📋 Your Personalized Learning Roadmap")
                                st.markdown(roadmap['roadmap'])
                                
                                st.success("✅ Roadmap saved to your profile!")
                            else:
                                st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
                        except Exception as e:
                            st.error(f"Connection error: {str(e)}")
                else:
                    st.success("🎉 You already have all the required skills!")
        else:
            st.info("👆 Complete the Skills Analysis first to generate a roadmap")
        
        # Show saved roadmaps
        st.markdown("---")
        st.subheader("📚 Saved Roadmaps")
        try:
            response = requests.get(f"{API_BASE_URL}/career/roadmaps/{st.session_state.user_id}")
            if response.status_code == 200:
                roadmaps = response.json()['roadmaps']
                
                if roadmaps:
                    for roadmap in roadmaps:
                        with st.expander(f"🎯 {roadmap['target_role']} - {roadmap['created_at']}"):
                            st.markdown(roadmap['generated_plan'])
                else:
                    st.info("No roadmaps saved yet")
        except:
            st.warning("Could not load roadmaps")

# ==================== ANALYTICS PAGE ====================
elif page == "📊 Analytics":
    st.title("📊 Learning Analytics")
    st.markdown("Track your learning progress and performance over time")
    
    try:
        # Fetch quiz results
        quiz_response = requests.get(f"{API_BASE_URL}/quiz/results/{st.session_state.user_id}")
        
        if quiz_response.status_code == 200:
            quiz_results = quiz_response.json()['results']
            
            if quiz_results:
                # Quiz performance chart
                st.subheader("📈 Quiz Performance Over Time")
                
                topics = [r['topic'] for r in quiz_results]
                scores = [(r['score'] / r['total'] * 100) for r in quiz_results]
                timestamps = [r['timestamp'] for r in quiz_results]
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=list(range(len(scores))),
                    y=scores,
                    mode='lines+markers',
                    name='Score',
                    line=dict(color='#1E88E5', width=3),
                    marker=dict(size=10)
                ))
                fig.add_hline(y=70, line_dash="dash", line_color="green", annotation_text="Pass Mark (70%)")
                fig.update_layout(
                    xaxis_title="Quiz Number",
                    yaxis_title="Score (%)",
                    yaxis_range=[0, 100],
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Performance by topic
                st.subheader("📊 Performance by Topic")
                topic_scores = {}
                for r in quiz_results:
                    topic = r['topic']
                    score_pct = (r['score'] / r['total'] * 100)
                    if topic not in topic_scores:
                        topic_scores[topic] = []
                    topic_scores[topic].append(score_pct)
                
                avg_scores = {topic: sum(scores)/len(scores) for topic, scores in topic_scores.items()}
                
                fig2 = go.Figure(data=[
                    go.Bar(
                        x=list(avg_scores.keys()),
                        y=list(avg_scores.values()),
                        marker_color='#1E88E5'
                    )
                ])
                fig2.update_layout(
                    xaxis_title="Topic",
                    yaxis_title="Average Score (%)",
                    yaxis_range=[0, 100],
                    height=400
                )
                st.plotly_chart(fig2, use_container_width=True)
                
                # Summary statistics
                st.subheader("📋 Summary Statistics")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Total Quizzes", len(quiz_results))
                with col2:
                    avg_score = sum(scores) / len(scores)
                    st.metric("Average Score", f"{avg_score:.1f}%")
                with col3:
                    passed = sum(1 for s in scores if s >= 70)
                    st.metric("Quizzes Passed", passed)
                with col4:
                    st.metric("Best Score", f"{max(scores):.1f}%")
            else:
                st.info("📝 No quiz data yet. Take some quizzes to see your analytics!")
        
        # Skills overview
        st.markdown("---")
        st.subheader("🎯 Skills Overview")
        skills_response = requests.get(f"{API_BASE_URL}/career/skills/{st.session_state.user_id}")
        
        if skills_response.status_code == 200:
            skills = skills_response.json()['skills']
            
            if skills:
                skill_names = [s['name'] for s in skills]
                st.markdown("**Your Skills:**")
                for skill in skill_names:
                    st.markdown(f"- {skill}")
            else:
                st.info("Complete a skills analysis to see your skills here")
    
    except Exception as e:
        st.error(f"Could not load analytics. Make sure backend is running on port 8000")
        st.error(f"Error details: {str(e)}")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>Made with ❤️ for Hackathon | EduMentor AI © 2026</div>",
    unsafe_allow_html=True
)
