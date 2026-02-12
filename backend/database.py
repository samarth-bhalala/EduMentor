"""
Database configuration and table initialization for EduMentor AI
"""
import sqlite3
from datetime import datetime
import os

DB_PATH = "data/db.sqlite"

def get_db_connection():
    """Get SQLite database connection"""
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Initialize database tables on startup"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            goal TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Documents table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            file_name TEXT NOT NULL,
            upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    
    # Quiz results table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quiz_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            topic TEXT NOT NULL,
            score INTEGER NOT NULL,
            total INTEGER NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    
    # Skills table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            skill_name TEXT NOT NULL,
            proficiency_level TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    
    # Roadmaps table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS roadmaps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            target_role TEXT NOT NULL,
            generated_plan TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    
    conn.commit()
    conn.close()
    print("✅ Database initialized successfully")

def create_user(name: str, email: str, goal: str = None):
    """Create a new user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "INSERT INTO users (name, email, goal) VALUES (?, ?, ?)",
            (name, email, goal)
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return user_id
    except sqlite3.IntegrityError:
        # User already exists, return existing user
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        user_id = cursor.fetchone()[0]
        conn.close()
        return user_id

def get_user_by_email(email: str):
    """Get user by email"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    return dict(user) if user else None

# Initialize on startup
init_database()

# Get connection
conn = get_db_connection()
cursor = conn.cursor()
cursor.execute("SELECT * FROM users")
users = cursor.fetchall()
# Each row is a dictionary-like object
