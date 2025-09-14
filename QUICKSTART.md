# Quick Start Guide

## Automation Project with Auto Clip Uploader

This automation project includes a powerful **Auto Clip Uploader** that processes long videos and automatically creates short clips for YouTube.

## 🚀 Quick Setup

### 1. Install Dependencies
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install FFmpeg (required for video processing)
# Windows: 
winget install Gyan.FFmpeg
# Or download from: https://ffmpeg.org/download.html
```

### 2. Run Setup Script (Optional)
```bash
python scripts/setup.py
```

### 3. Configure YouTube API (for uploads)
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable YouTube Data API v3
4. Create OAuth 2.0 credentials (Desktop application)
5. Download as `client_secret.json` and place in project root

## 📋 Available Tasks

### Basic Framework Tasks
```bash
# List all available tasks
python src/main.py --list-tasks

# Run hello world task
python src/main.py --task hello_world

# Run system check
python src/main.py --task system_check

# Run cleanup task  
python src/main.py --task cleanup
```

### Auto Clip Uploader Task
```bash
# Configure video URL first in config/default.json:
# "task_settings.clip_uploader.video_url": "https://your-video-url.mp4"
# "task_settings.clip_uploader.enabled": true

# Run clip uploader (dry run by default)
python src/main.py --task clip_uploader
```

## 🎬 Auto Clip Uploader Features

✅ **Scene Detection** - Uses FFmpeg to detect scene changes  
✅ **Smart Clipping** - Extracts clips based on scene boundaries  
✅ **AI Transcription** - Uses Whisper for free speech-to-text  
✅ **Auto Metadata** - Generates titles, descriptions, and tags  
✅ **YouTube Upload** - Direct upload to YouTube  
✅ **Free Stack** - All tools are free (except YouTube API quota)

## ⚙️ Configuration

Edit `config/default.json`:

```json
{
    "task_settings": {
        "clip_uploader": {
            "enabled": true,
            "video_url": "https://example.com/your-video.mp4",
            "dry_run": false,
            "max_clips": 6,
            "whisper_model": "tiny",
            "scene_threshold": 0.4
        }
    }
}
```

## 🔧 Direct Usage (Alternative)

```bash
# Use clip uploader directly (dry run)
python src/auto_clip_uploader.py "https://video-url.mp4" --dry-run

# Process and upload to YouTube
python src/auto_clip_uploader.py "https://video-url.mp4"
```

## 📁 Project Structure

```
automation-project/
├── src/                    # Source code
│   ├── main.py            # Main automation framework
│   ├── automation_framework.py
│   ├── config_manager.py
│   └── auto_clip_uploader.py  # Auto clip uploader
├── config/                # Configuration files
│   └── default.json      # Main config
├── docs/                  # Documentation
│   └── AUTO_CLIP_UPLOADER.md  # Detailed docs
├── tests/                 # Test files
├── scripts/              # Utility scripts
│   └── setup.py         # Setup script
├── videos/               # Generated video clips
│   ├── clips/           # Output clips
│   └── tmp/             # Temporary files
├── logs/                 # Log files
├── requirements.txt      # Python dependencies
├── README.md            # Main project README
└── QUICKSTART.md       # This file
```

## ⚠️ Important Notes

### Before Using Auto Clip Uploader:
- ✅ Install FFmpeg and ensure it's in PATH
- ✅ Install Python dependencies: `pip install -r requirements.txt`
- ✅ Set up YouTube API credentials (client_secret.json)
- ✅ Only process videos you own or have permission to use
- ✅ Test with dry_run: true first
- ✅ Review YouTube's content policies

### First Run:
- Browser will open for YouTube authorization
- Whisper will download model weights (~39MB for "tiny")
- Processing time depends on video length and model size

## 🎯 Quick Test

1. **Test basic framework:**
   ```bash
   python src/main.py --task hello_world
   ```

2. **Test with a sample video (dry run):**
   ```bash
   # Edit config/default.json to set a video URL and enable the task
   python src/main.py --task clip_uploader
   ```

3. **Check generated clips:**
   ```bash
   dir videos\clips
   ```

## 🔗 Useful Links

- [FFmpeg Download](https://ffmpeg.org/download.html)
- [Google Cloud Console](https://console.cloud.google.com/)
- [YouTube Data API](https://developers.google.com/youtube/v3)
- [Whisper Models](https://github.com/openai/whisper#available-models-and-languages)

## 🆘 Need Help?

- Check `logs/automation.log` for detailed logs
- See `docs/AUTO_CLIP_UPLOADER.md` for comprehensive documentation
- Test with `--log-level DEBUG` for verbose output
- Always start with `dry_run: true` for testing

---

**Ready to automate your video content creation!** 🎉