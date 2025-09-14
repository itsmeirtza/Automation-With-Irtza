# 🚀 Automation With Irtza - Setup Guide

**Created by: Irtza Ali Waris**  
**Email:** Irtzaaliwaris@gmail.com  
**Website:** https://ialiwaris.com

## 📋 Overview

Automation With Irtza is a comprehensive video automation framework that:
- Takes YouTube channel links and video URLs
- Uses AI to automatically detect scenes and create clips
- Generates 6 video previews for review
- Uploads selected clips to YouTube with automated metadata
- Provides a beautiful dashboard for monitoring all processes

## 🔧 Prerequisites

### 1. Python 3.8+
Download and install Python from: https://python.org
- Make sure to check "Add Python to PATH" during installation

### 2. FFmpeg
Download FFmpeg from: https://ffmpeg.org/download.html
- For Windows: Download the executable and add to system PATH
- For Mac: `brew install ffmpeg`
- For Linux: `sudo apt install ffmpeg`

### 3. YouTube API Setup
1. Go to: https://console.developers.google.com
2. Create a new project or select existing one
3. Enable YouTube Data API v3
4. Create OAuth 2.0 credentials
5. Download the client configuration as `client_secret.json`
6. Place `client_secret.json` in the project root directory

## 🚀 Installation

### Step 1: Install Dependencies
```bash
# Install Python packages
pip install -r requirements.txt
```

### Step 2: Verify Installation
```bash
# Run the application
python run.py
```

## 📱 How to Use

### Method 1: Web Interface (Recommended)
1. Run: `python run.py`
2. Open browser to: `http://localhost:5000`
3. Follow the 6-step workflow:
   - **Step 1:** Enter YouTube channel link
   - **Step 2:** Enter video URL to process
   - **Step 3:** Wait for AI processing (automatic)
   - **Step 4:** Preview and select clips (up to 6)
   - **Step 5:** Upload to YouTube (automatic)
   - **Step 6:** View results in dashboard

### Method 2: Command Line
```bash
# Process a video (dry run - no upload)
python -m src.main --task clip_uploader

# Run specific automation task
python -m src.main --task system_check

# List all available tasks
python -m src.main --list-tasks
```

## 🌐 Web Interface

### Main Workflow: `http://localhost:5000`
Beautiful step-by-step interface that guides you through:
1. YouTube channel setup
2. Video processing
3. Clip preview and selection
4. Automated uploading

### Dashboard: `http://localhost:5000/dashboard`
Comprehensive monitoring panel showing:
- System statistics
- Recent activity
- Processed clips
- Control panel
- Real-time status updates

## ⚙️ Configuration

### config/default.json
```json
{
  "default_workflow": ["clip_uploader"],
  "task_settings": {
    "clip_uploader": {
      "enabled": true,
      "dry_run": false,
      "video_url": "https://www.youtube.com/watch?v=YOUR_VIDEO_ID",
      "max_clips": 6,
      "whisper_model": "tiny",
      "scene_threshold": 0.4
    }
  }
}
```

## 🎯 Features

### AI-Powered Video Processing
- **Scene Detection:** Automatically finds natural break points in videos
- **Whisper Transcription:** Uses OpenAI's Whisper for accurate audio transcription
- **Smart Metadata:** Generates titles, descriptions, and tags using TF-IDF analysis

### Intelligent Workflow
- **Step-by-step Process:** Clear 6-step workflow for easy use
- **Preview System:** Review all clips before uploading
- **Selective Upload:** Choose which clips to upload to YouTube
- **Real-time Monitoring:** Live progress updates and status tracking

### Professional Dashboard
- **System Statistics:** Monitor performance and usage
- **Activity Logging:** Track all automation activities
- **Clip Management:** View and manage processed videos
- **Control Panel:** Easy access to all system functions

## 📁 Project Structure

```
automation-project/
├── src/                          # Core automation code
│   ├── auto_clip_uploader.py    # Main video processing logic
│   ├── automation_framework.py  # Framework orchestration
│   ├── config_manager.py        # Configuration management
│   └── main.py                  # CLI entry point
├── website/                     # Static website files
│   ├── index.html              # Original landing page
│   ├── css/                    # Stylesheets
│   └── js/                     # JavaScript files
├── templates/                   # Flask templates
│   ├── workflow.html           # Step-by-step workflow interface
│   └── dashboard.html          # Dashboard interface
├── config/                     # Configuration files
│   └── default.json           # Default settings
├── videos/                     # Video processing directories
│   ├── clips/                 # Generated clips
│   └── tmp/                   # Temporary files
├── logs/                       # Application logs
├── uploads/                    # Upload directory
├── app.py                     # Flask web application
├── run.py                     # Startup script
├── requirements.txt           # Python dependencies
├── client_secret.json         # YouTube API credentials (you provide)
└── README.md                  # Project documentation
```

## 🔧 Troubleshooting

### Python Not Found
- Install Python 3.8+ from python.org
- Make sure Python is added to system PATH
- Try using `py` instead of `python` on Windows

### FFmpeg Not Found
- Download FFmpeg from ffmpeg.org
- Add FFmpeg to system PATH
- Restart terminal/command prompt after installation

### YouTube API Errors
- Ensure client_secret.json is in project root
- Check YouTube Data API v3 is enabled in Google Console
- Verify OAuth consent screen is configured

### Dependencies Missing
```bash
# Install all required packages
pip install -r requirements.txt

# If specific package fails, install individually
pip install flask werkzeug jinja2 openai-whisper scikit-learn
```

### Permission Errors
- Run terminal/command prompt as Administrator (Windows)
- Use `sudo` for installation commands (Mac/Linux)
- Check file/folder permissions

## 📊 Performance Tips

### For Better Performance:
- Use smaller Whisper models ("tiny", "small") for faster transcription
- Adjust scene_threshold (0.3-0.5) for different video types
- Process shorter videos first to test setup
- Ensure good internet connection for YouTube uploads

### Optimize Settings:
```python
# In auto_clip_uploader.py, adjust these constants:
WHISPER_MODEL = "tiny"        # Fastest model
SCENE_THRESHOLD = 0.4         # Good balance
MAX_CLIPS_PER_RUN = 6         # Reasonable limit
MIN_CLIP_SECONDS = 5          # Minimum clip length
MAX_CLIP_SECONDS = 180        # Maximum clip length (3 minutes)
```

## 🚀 Getting Started (Quick)

1. **Install Python 3.8+** and **FFmpeg**
2. **Download** this project
3. **Get YouTube API credentials** (`client_secret.json`)
4. **Install dependencies:** `pip install -r requirements.txt`
5. **Run:** `python run.py`
6. **Open:** `http://localhost:5000`
7. **Start automating!** 🎉

## 📞 Support

**Created by:** Irtza Ali Waris  
**Email:** Irtzaaliwaris@gmail.com  
**Website:** https://ialiwaris.com

For issues or questions:
1. Check this guide first
2. Review error messages carefully
3. Contact Irtza directly via email

---

## 🎉 Ready to Automate!

Your video automation framework is now set up and ready to use. Visit `http://localhost:5000` to begin creating automated video clips with AI-powered processing!

**Happy Automating! 🚀**