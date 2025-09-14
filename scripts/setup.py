"""
Setup script for the automation project.

This script helps set up the environment and dependencies.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("ERROR: Python 3.8 or higher is required")
        return False
    print(f"✓ Python version: {sys.version}")
    return True

def check_ffmpeg():
    """Check if ffmpeg is installed and accessible."""
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ ffmpeg is installed and accessible")
            return True
    except FileNotFoundError:
        pass
    
    print("⚠ ffmpeg not found. Please install ffmpeg and add it to PATH")
    print("  Windows: Download from https://ffmpeg.org/download.html")
    print("  Or use: winget install Gyan.FFmpeg")
    return False

def install_dependencies():
    """Install Python dependencies."""
    requirements_file = Path(__file__).parent.parent / "requirements.txt"
    
    if not requirements_file.exists():
        print("ERROR: requirements.txt not found")
        return False
    
    print("Installing Python dependencies...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', str(requirements_file)])
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("ERROR: Failed to install dependencies")
        return False

def create_directories():
    """Create necessary directories."""
    project_root = Path(__file__).parent.parent
    directories = [
        project_root / "logs",
        project_root / "videos",
        project_root / "videos" / "clips",
        project_root / "videos" / "tmp"
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
    
    print("✓ Directories created")
    return True

def setup_git_hooks():
    """Set up basic git hooks if in a git repository."""
    project_root = Path(__file__).parent.parent
    git_dir = project_root / ".git"
    
    if not git_dir.exists():
        print("⚠ Not a git repository, skipping git hooks setup")
        return True
    
    print("✓ Git repository detected")
    return True

def main():
    """Main setup function."""
    print("🚀 Setting up Automation Project...")
    print("=" * 50)
    
    success = True
    
    # Check Python version
    if not check_python_version():
        success = False
    
    # Check ffmpeg
    if not check_ffmpeg():
        success = False
    
    # Install dependencies
    if not install_dependencies():
        success = False
    
    # Create directories
    if not create_directories():
        success = False
    
    # Setup git hooks
    if not setup_git_hooks():
        success = False
    
    print("=" * 50)
    if success:
        print("✅ Setup completed successfully!")
        print("\nNext steps:")
        print("1. To run the automation framework:")
        print("   python src/main.py --list-tasks")
        print("2. To use the auto clip uploader:")
        print("   - Install ffmpeg if not already done")
        print("   - Add your YouTube OAuth client_secret.json")
        print("   - Configure video URL in config/default.json")
        print("   - Run: python src/main.py --task clip_uploader")
        print("3. Run tests:")
        print("   python -m pytest tests/")
    else:
        print("❌ Setup failed. Please fix the errors above and try again.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())