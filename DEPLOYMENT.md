# 🚀 Deployment Guide for Multi-Agent AI System

This guide covers deploying the Multi-Agent AI System to GitHub and Streamlit Cloud.

## 📋 Prerequisites

- Git installed on your system
- GitHub account
- Streamlit Cloud account (free at share.streamlit.io)

## 🐙 GitHub Deployment

### Step 1: Initialize Git Repository

```bash
# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Multi-Agent AI System"
```

### Step 2: Create GitHub Repository

1. Go to [GitHub.com](https://github.com)
2. Click "New Repository"
3. Name it: `multi-agent-ai-system`
4. Set to Public (required for free Streamlit deployment)
5. Don't initialize with README (we already have one)
6. Click "Create Repository"

### Step 3: Push to GitHub

```bash
# Add GitHub remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/multi-agent-ai-system.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## ☁️ Streamlit Cloud Deployment

### Step 1: Access Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Authorize Streamlit to access your repositories

### Step 2: Deploy the App

1. Click "New app"
2. Select your repository: `YOUR_USERNAME/multi-agent-ai-system`
3. Set branch: `main`
4. Set main file path: `streamlit_app.py`
5. Click "Deploy!"

### Step 3: Configuration

The app will automatically:
- Install dependencies from `streamlit_requirements.txt`
- Use configuration from `.streamlit/config.toml`
- Start the Streamlit frontend

## ⚠️ Important Notes for Cloud Deployment

### Backend Limitations
- **Streamlit Cloud only runs the frontend**
- The backend (FastAPI) requires a separate hosting service
- For full functionality, consider:
  - **Heroku** (backend deployment)
  - **Railway** (full-stack deployment)
  - **Google Cloud Run** (containerized deployment)

### Streamlit-Only Mode
The current deployment will run in "demo mode" with:
- ✅ File upload interface
- ✅ Chat interface
- ❌ Limited backend processing (no API calls)
- ✅ Sample data demonstrations

## 🔧 Full Production Deployment Options

### Option 1: Heroku (Backend) + Streamlit Cloud (Frontend)

**Backend on Heroku:**
```bash
# Install Heroku CLI
# Create Procfile for backend
echo "web: uvicorn backend.main:app --host 0.0.0.0 --port $PORT" > Procfile

# Deploy to Heroku
heroku create your-app-backend
git push heroku main
```

**Update Frontend:**
```python
# In frontend/app.py, change API_BASE_URL to:
API_BASE_URL = "https://your-app-backend.herokuapp.com"
```

### Option 2: Railway (Full Stack)

1. Connect your GitHub repo to Railway
2. Deploy backend and frontend as separate services
3. Configure environment variables

### Option 3: Google Cloud Run

```bash
# Build and deploy backend
gcloud run deploy multiagent-backend \
  --source ./backend \
  --platform managed \
  --region us-central1

# Deploy frontend with updated API URL
gcloud run deploy multiagent-frontend \
  --source ./frontend \
  --platform managed \
  --region us-central1
```

## 🎯 Quick Demo Deployment (Streamlit Only)

For a quick demo that showcases the UI and basic functionality:

1. **GitHub**: Push your code
2. **Streamlit Cloud**: Deploy `streamlit_app.py`
3. **Demo Mode**: Show file upload, chat interface, and sample interactions

This gives you a live demo URL to share immediately!

## 📱 Sharing Your Demo

Once deployed on Streamlit Cloud, you'll get:
- **Public URL**: `https://your-username-multi-agent-ai-system-streamlit-app-xyz.streamlit.app`
- **Easy sharing**: Send the link to anyone
- **Live updates**: Pushes to GitHub auto-deploy

## 🔍 Monitoring and Analytics

Streamlit Cloud provides:
- **Usage analytics**: Visitor statistics
- **Error monitoring**: Runtime error tracking
- **Performance metrics**: Load times and usage patterns

## 🛠️ Troubleshooting

### Common Issues:

**1. Dependencies not installing:**
- Check `streamlit_requirements.txt` format
- Ensure all packages are available on PyPI

**2. Import errors:**
- Verify file paths in `streamlit_app.py`
- Check Python path configurations

**3. Large model downloads:**
- Sentence transformers may take time on first load
- Consider using lighter models for demo

**4. Memory limits:**
- Streamlit Cloud has memory constraints
- Optimize data processing for cloud deployment

## 🎉 Success!

Once deployed, your Multi-Agent AI System will be:
- ✅ **Publicly accessible**
- ✅ **Automatically updated** with GitHub pushes
- ✅ **Professional presentation** ready
- ✅ **Demo-ready** for your assignment

---

**Next Steps**: Follow the GitHub deployment steps, then deploy to Streamlit Cloud for an instant live demo!
