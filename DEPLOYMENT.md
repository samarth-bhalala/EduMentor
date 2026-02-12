# Streamlit Cloud Deployment Guide

## 🚀 Quick Deploy to Streamlit Cloud

### Option 1: Deploy Frontend Only (Recommended for Demo)

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Ready for Streamlit deployment"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your GitHub repository
   - Main file: `app.py`
   - Click "Deploy"

3. **Set Environment Variables (Optional)**
   - In Streamlit Cloud dashboard, go to "Settings" → "Secrets"
   - Add your Hugging Face token:
     ```toml
     HF_TOKEN = "your_token_here"
     ```

### ⚠️ Important Notes for Streamlit Cloud

**Backend Limitations:**
- Streamlit Cloud only runs the frontend (`app.py`)
- The FastAPI backend won't run on Streamlit Cloud
- You have two options:

#### Option A: Deploy Backend Separately (Full Functionality)
1. Deploy FastAPI backend on:
   - **Render.com** (Free tier available)
   - **Railway.app** (Free tier available)
   - **Heroku** (Paid)
   
2. Update `API_BASE_URL` in `app.py`:
   ```python
   API_BASE_URL = "https://your-backend-url.com"
   ```

#### Option B: Frontend-Only Mode (Limited Demo)
- Add a note in the app that it's a frontend demo
- Features will show errors without backend
- Good for UI/UX demonstration

### 📋 Files for Deployment

**Required files:**
- ✅ `app.py` - Main Streamlit app
- ✅ `requirements.txt` - Python dependencies
- ✅ `packages.txt` - System dependencies (if needed)
- ✅ `.streamlit/config.toml` - Streamlit configuration

**Key Changes Made:**
1. Downgraded `faiss-cpu` to 1.7.4 (better Streamlit Cloud compatibility)
2. Added `numpy<2.0.0` constraint
3. Added `torch==2.1.0` explicitly
4. Created `packages.txt` for system dependencies
5. Created `.streamlit/config.toml` for configuration

### 🐛 Common Deployment Issues

**Issue: "installer returned a non-zero exit code"**
- ✅ **Fixed**: Used compatible package versions
- ✅ **Fixed**: Added numpy constraint
- ✅ **Fixed**: Removed sqlalchemy (not needed for frontend)

**Issue: Backend connection errors**
- Expected if backend isn't deployed separately
- Update `API_BASE_URL` to point to your deployed backend

**Issue: Missing HF_TOKEN**
- Add token in Streamlit Cloud secrets
- Or modify code to work without token (free tier, rate limited)

### 🔧 Deploy Backend on Render.com (Free)

1. Create `render.yaml`:
   ```yaml
   services:
     - type: web
       name: edumentor-backend
       env: python
       buildCommand: pip install -r requirements.txt
       startCommand: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
   ```

2. Push to GitHub and connect to Render
3. Set environment variable: `HF_TOKEN`
4. Update frontend `API_BASE_URL`

### 📝 Alternative: Full Local Demo

If deployment is too complex for hackathon:
```bash
# Terminal 1: Backend
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000

# Terminal 2: Frontend  
python -m streamlit run app.py
```

Then use **ngrok** to create public URLs:
```bash
ngrok http 8000  # For backend
ngrok http 8501  # For frontend
```

### ✅ Deployment Checklist

- [x] Fixed requirements.txt for Streamlit Cloud
- [x] Created packages.txt
- [x] Created .streamlit/config.toml
- [ ] Push to GitHub
- [ ] Deploy to Streamlit Cloud
- [ ] (Optional) Deploy backend separately
- [ ] (Optional) Update API_BASE_URL
- [ ] Add HF_TOKEN in secrets

### 🎯 For Hackathon Demo

**Best approach:**
1. Deploy frontend to Streamlit Cloud (shows nice UI)
2. Run backend locally during presentation
3. Use ngrok to expose local backend
4. Update `API_BASE_URL` to ngrok URL temporarily

This gives you:
- ✅ Professional hosted frontend
- ✅ Full functionality during demo
- ✅ No complex backend deployment needed

---

**Need Help?** Check the error logs in Streamlit Cloud dashboard under "Manage app" → "Logs"
