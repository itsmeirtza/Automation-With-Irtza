# Auto Clip Uploader Documentation

## Overview

The Auto Clip Uploader is a powerful automation tool that processes long-form videos and automatically creates engaging short clips for YouTube. It uses AI-powered scene detection, transcription, and metadata generation to create high-quality content efficiently.

## Features

- **Scene Detection**: Uses FFmpeg to detect scene changes in videos without downloading the entire file
- **Smart Clipping**: Extracts clips based on scene boundaries with configurable duration limits
- **AI Transcription**: Uses OpenAI's Whisper (local models) for free speech-to-text conversion
- **Metadata Generation**: Automatically generates titles, descriptions, and tags using TF-IDF analysis
- **YouTube Integration**: Uploads clips directly to YouTube using the YouTube Data API
- **Free Stack**: Uses only free and open-source tools (except YouTube API quota)

## Prerequisites

### Required Software
1. **Python 3.8+**: The automation framework requires Python 3.8 or higher
2. **FFmpeg**: Must be installed and accessible in PATH
   - Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html) or use `winget install Gyan.FFmpeg`
   - macOS: `brew install ffmpeg`
   - Linux: `sudo apt-get install ffmpeg` or equivalent

### Required Dependencies
Install via pip:
```bash
pip install -r requirements.txt
```

Key dependencies:
- `openai-whisper`: For audio transcription
- `scikit-learn`: For TF-IDF metadata generation
- `google-api-python-client`: For YouTube API integration
- `google-auth-oauthlib`: For YouTube OAuth authentication

### YouTube API Setup
1. Create a Google Cloud Project
2. Enable the YouTube Data API v3
3. Create OAuth 2.0 credentials (Desktop application)
4. Download the client configuration as `client_secret.json`
5. Place `client_secret.json` in the project root directory

## Installation and Setup

### Quick Setup
Run the automated setup script:
```bash
python scripts/setup.py
```

### Manual Setup
1. Clone or download the project
2. Install dependencies: `pip install -r requirements.txt`
3. Create necessary directories:
   ```bash
   mkdir -p videos/clips videos/tmp logs
   ```
4. Configure the application (see Configuration section)

## Configuration

### Basic Configuration
Edit `config/default.json` to configure the clip uploader:

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

### Configuration Options
- `enabled`: Enable/disable the clip uploader task
- `video_url`: URL of the video to process
- `dry_run`: If true, creates clips but doesn't upload to YouTube
- `max_clips`: Maximum number of clips to create per run (default: 6)
- `whisper_model`: Whisper model size ("tiny", "small", "base", "large")
- `scene_threshold`: Scene detection sensitivity (0.1-0.6, higher = fewer scenes)

### Advanced Configuration
You can also configure clip duration limits and other parameters by modifying the `AutoClipUploader` class constants:

```python
MIN_CLIP_SECONDS = 5      # Minimum clip duration
MAX_CLIP_SECONDS = 180    # Maximum clip duration  
SCENE_THRESHOLD = 0.4     # Scene detection threshold
```

## Usage

### Through Automation Framework
The recommended way to use the clip uploader:

```bash
# List available tasks
python src/main.py --list-tasks

# Run clip uploader task
python src/main.py --task clip_uploader

# Run with custom config
python src/main.py --config config/custom.json --task clip_uploader
```

### Direct Usage
You can also run the clip uploader directly:

```bash
# Process video (dry run by default)
python src/auto_clip_uploader.py "https://example.com/video.mp4" --dry-run

# Process and upload to YouTube
python src/auto_clip_uploader.py "https://example.com/video.mp4"
```

### First Run Authorization
On the first run, the system will:
1. Open your default web browser
2. Prompt you to sign in to your Google account
3. Ask for permission to upload videos to YouTube
4. Save the authorization token for future use

## How It Works

### Processing Pipeline
1. **Scene Detection**: FFmpeg analyzes the video stream to detect scene changes
2. **Clip Selection**: Algorithm selects optimal clip boundaries based on scenes
3. **Clip Extraction**: FFmpeg extracts individual clips without downloading the full video
4. **Transcription**: Whisper transcribes audio content to text
5. **Metadata Generation**: TF-IDF analysis generates titles, descriptions, and tags
6. **Upload**: Clips are uploaded to YouTube with generated metadata

### Scene Detection
The tool uses FFmpeg's scene detection filter:
- Analyzes pixel differences between frames
- Identifies significant visual changes
- Configurable threshold (0.1 = sensitive, 0.6 = less sensitive)
- No full video download required

### Transcription Process
- Uses OpenAI's Whisper for local, free transcription
- Model downloads automatically on first use
- Supports multiple model sizes (tiny, small, base, large)
- Processes audio tracks from video clips

### Metadata Generation
- Extracts keywords using TF-IDF (Term Frequency-Inverse Document Frequency)
- Generates engaging titles from top keywords
- Creates descriptions with hashtags
- Provides relevant tags for YouTube SEO

## Output and Results

### File Structure
```
automation-project/
├── videos/
│   ├── clips/           # Generated video clips
│   │   ├── clip_001.mp4
│   │   ├── clip_002.mp4
│   │   └── ...
│   └── tmp/             # Temporary files
├── logs/
│   └── automation.log   # Detailed processing logs
└── ...
```

### Results Summary
After processing, you'll see a summary including:
- Number of clips created
- Number of clips successfully uploaded
- Any errors encountered
- YouTube video IDs for uploaded content

## Troubleshooting

### Common Issues

#### FFmpeg Not Found
```
Error: ffmpeg not found
```
**Solution**: Install FFmpeg and ensure it's in your system PATH

#### Missing Dependencies
```
Error: Missing dependencies: whisper, scikit-learn
```
**Solution**: Run `pip install -r requirements.txt`

#### YouTube API Errors
```
Error: client_secret.json missing
```
**Solution**: Set up YouTube API credentials and place client_secret.json in project root

#### Quota Exceeded
```
Error: YouTube API quota exceeded
```
**Solution**: YouTube API has daily limits. Wait until quota resets or request quota increase

### Debug Mode
Enable detailed logging:
```bash
python src/main.py --log-level DEBUG --task clip_uploader
```

### Dry Run Testing
Always test with dry run first:
```json
{
    "clip_uploader": {
        "dry_run": true
    }
}
```

## Best Practices

### Content Guidelines
- **Copyright**: Only process videos you own or have permission to use
- **Content Policy**: Ensure clips comply with YouTube's community guidelines
- **Manual Review**: Consider adding manual review before automatic upload

### Performance Optimization
- Use "tiny" Whisper model for speed, "small" or "base" for accuracy
- Adjust scene threshold based on video content type
- Limit max_clips to avoid API quota issues

### API Management
- Monitor YouTube API quota usage
- Use dry run for testing
- Consider batch processing during off-peak hours

## API Limits and Costs

### YouTube Data API v3
- **Free Quota**: 10,000 units per day
- **Upload Cost**: ~1,600 units per video
- **Daily Limit**: ~6 uploads per day with standard quota

### Local Processing (Free)
- FFmpeg: Free and open source
- Whisper: Free local models
- TF-IDF: Free analysis

## Advanced Usage

### Custom Tasks Integration
Extend the automation framework with custom tasks:

```python
def custom_clip_processor(self) -> bool:
    uploader = AutoClipUploader()
    results = uploader.process_video(url, dry_run=False)
    # Custom processing logic
    return True

# Add to automation framework
framework.add_custom_task("custom_processor", custom_clip_processor)
```

### Batch Processing
Process multiple videos:
```python
urls = ["url1", "url2", "url3"]
for url in urls:
    config["task_settings"]["clip_uploader"]["video_url"] = url
    framework.run_task("clip_uploader")
```

## License and Legal

### Software License
This project is licensed under the MIT License.

### Important Legal Notes
- **Copyright Compliance**: Only process content you own or have rights to
- **YouTube Terms**: Comply with YouTube's Terms of Service
- **Content Policy**: Ensure uploaded content meets platform guidelines
- **API Terms**: Follow Google APIs Terms of Service

## Support and Contributing

### Getting Help
- Check the logs in `logs/automation.log`
- Review configuration settings
- Test with dry run mode first
- Check FFmpeg installation and PATH

### Contributing
Contributions are welcome! Areas for improvement:
- Manual approval UI
- Better scene scoring algorithms
- LLM integration for metadata generation
- Support for additional platforms

## Version History

### v1.0.0
- Initial release with core functionality
- FFmpeg scene detection
- Whisper transcription
- TF-IDF metadata generation
- YouTube API integration
- Automation framework integration