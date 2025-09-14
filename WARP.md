# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This is a Python-based automation framework with a focus on video content processing. The project includes a flexible task-based automation system and a specialized **Auto Clip Uploader** that converts long-form videos into short clips for YouTube using AI-powered scene detection and transcription.

## Common Development Commands

### Setup and Environment
```bash
# Initial setup (checks dependencies, creates directories)
python scripts/setup.py

# Install Python dependencies
pip install -r requirements.txt

# Install FFmpeg (Windows - required for video processing)
winget install Gyan.FFmpeg
```

### Running the Application
```bash
# List available automation tasks
python src/main.py --list-tasks

# Run specific tasks
python src/main.py --task hello_world
python src/main.py --task system_check
python src/main.py --task cleanup
python src/main.py --task clip_uploader

# Run with custom configuration
python src/main.py --config config/custom.json --task clip_uploader

# Debug mode with verbose logging
python src/main.py --task clip_uploader --log-level DEBUG
```

### Auto Clip Uploader Direct Usage
```bash
# Process video with dry run (safe testing)
python src/auto_clip_uploader.py "https://video-url.mp4" --dry-run

# Process and upload to YouTube
python src/auto_clip_uploader.py "https://video-url.mp4"
```

### Testing
```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_automation.py

# Run tests with verbose output
python -m pytest tests/ -v
```

## Code Architecture

### Core Framework Components

**AutomationFramework** (`src/automation_framework.py`)
- Main orchestrator class that manages task execution
- Task registry system with built-in tasks: `hello_world`, `system_check`, `cleanup`, `clip_uploader`
- Workflow execution engine with error handling and timing
- Extensible design for adding custom tasks via `add_custom_task()`

**ConfigManager** (`src/config_manager.py`)
- Centralized configuration management with JSON-based settings
- Support for hierarchical configuration keys (e.g., `task_settings.clip_uploader.enabled`)
- Dynamic configuration updates and persistent storage
- Fallback to default configuration if config file is missing

**Main Entry Point** (`src/main.py`)
- CLI interface with argparse for task execution and configuration
- Logging setup with both console and file output (`logs/automation.log`)
- Integration point between command-line arguments and framework components

### Auto Clip Uploader Architecture

**AutoClipUploader** (`src/auto_clip_uploader.py`)
- Self-contained video processing pipeline
- **Scene Detection**: Uses FFmpeg streaming to detect scene changes without full download
- **Clip Extraction**: Streams specific portions of video using FFmpeg seek operations
- **Transcription Pipeline**: Integrates OpenAI Whisper for local speech-to-text
- **Metadata Generation**: TF-IDF analysis for generating YouTube titles, descriptions, and tags
- **YouTube Integration**: OAuth2 flow and video upload via YouTube Data API v3

### Configuration System

Configuration is centralized in `config/default.json` with the following key sections:
- `task_settings`: Per-task configuration including the clip uploader settings
- `automation_settings`: Framework-level settings (retries, timeouts)
- `default_workflow`: Task sequence for default execution

Critical clip uploader configuration:
- `video_url`: Source video URL for processing
- `dry_run`: Safety flag to prevent accidental uploads
- `max_clips`: Limit clips per execution (default: 6)
- `whisper_model`: AI model size ("tiny", "small", "base", "large")
- `scene_threshold`: Scene detection sensitivity (0.1-0.6)

### Directory Structure and Data Flow

```
src/                    # Core application code
├── main.py            # CLI entry point
├── automation_framework.py  # Task orchestration
├── config_manager.py  # Configuration management
└── auto_clip_uploader.py   # Video processing pipeline

config/                # Configuration files
└── default.json      # Main configuration

videos/                # Video processing workspace
├── clips/            # Output clips ready for upload
└── tmp/              # Temporary processing files

logs/                 # Application logs
└── automation.log    # Centralized logging
```

## Development Guidelines

### Adding New Tasks
1. Create task function in `AutomationFramework` following the `_taskname_task()` pattern
2. Register task in `_initialize_tasks()` method
3. Add task configuration section in `config/default.json` under `task_settings`
4. Include task in `default_workflow` array if it should run automatically

### YouTube API Integration Requirements
- Place `client_secret.json` (OAuth2 credentials) in project root
- First run requires interactive browser authentication
- Token stored as `token.pkl` for subsequent runs
- API quota limits apply (standard free tier limits)

### Video Processing Dependencies
- **FFmpeg**: Must be installed and accessible in system PATH
- **Whisper Models**: Downloaded automatically on first use (~39MB for "tiny" model)
- **Scene Detection**: Processes video streams without full downloads for efficiency

### Testing and Safety
- Always use `dry_run: true` for initial testing of clip uploader
- Check `logs/automation.log` for detailed execution information
- Verify FFmpeg installation with `ffmpeg -version`
- Test framework tasks before video processing: `python src/main.py --task hello_world`