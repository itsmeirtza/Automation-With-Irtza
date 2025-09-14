#!/usr/bin/env python3
"""
Automation With Irtza - Startup Script
Created by: Irtza Ali Waris
Email: Irtzaaliwaris@gmail.com
Website: https://ialiwaris.com

This script starts the Automation With Irtza web application.

To run this application:
1. Install Python 3.8+ from https://python.org
2. Install FFmpeg from https://ffmpeg.org/download.html
3. Run: pip install -r requirements.txt
4. Run: python run.py
5. Open browser to: http://localhost:5000
"""

import sys
import os
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is supported"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        print(f"Current version: {sys.version}")
        print("Please install Python 3.8+ from https://python.org")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} detected")
    return True

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'flask',
        'werkzeug',
        'jinja2',
        'whisper',
        'sklearn',
        'googleapiclient',
        'google_auth_oauthlib'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} is installed")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} is missing")
    
    if missing_packages:
        print(f"\n🔧 To install missing packages, run:")
        print(f"pip install -r requirements.txt")
        return False
    
    return True

def check_ffmpeg():
    """Check if FFmpeg is installed"""
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, 
                              text=True, 
                              check=True)
        print("✅ FFmpeg is installed")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ FFmpeg is not installed or not in PATH")
        print("Please install FFmpeg from: https://ffmpeg.org/download.html")
        print("Make sure ffmpeg.exe is in your system PATH")
        return False

def create_directories():
    """Create required directories"""
    directories = [
        'videos/clips',
        'videos/tmp',
        'logs',
        'uploads'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def show_banner():
    """Show application banner"""
    print("\n" + "="*60)
    print("    🚀 AUTOMATION WITH IRTZA - VIDEO AUTOMATION FRAMEWORK")
    print("="*60)
    print("    Created by: Irtza Ali Waris")
    print("    Email: Irtzaaliwaris@gmail.com")
    print("    Website: https://ialiwaris.com")
    print("="*60)

def main():
    """Main startup function"""
    show_banner()
    
    print("\n🔍 Checking system requirements...")
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check dependencies
    print("\n📦 Checking Python packages...")
    dependencies_ok = check_dependencies()
    
    # Check FFmpeg
    print("\n🎥 Checking FFmpeg...")
    ffmpeg_ok = check_ffmpeg()
    
    # Create directories
    print("\n📁 Creating directories...")
    create_directories()
    
    if not dependencies_ok:
        print("\n❌ Missing Python packages. Please install them first.")
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    if not ffmpeg_ok:
        print("\n⚠️  FFmpeg not found. Video processing may not work.")
        print("You can still run the application, but install FFmpeg for full functionality.")
        
        choice = input("\nDo you want to continue anyway? (y/N): ").strip().lower()
        if choice not in ['y', 'yes']:
            sys.exit(1)
    
    # Import and run the Flask application
    print("\n🚀 Starting Automation With Irtza...")
    print("📱 Web Interface: http://localhost:5000")
    print("📊 Dashboard: http://localhost:5000/dashboard")
    print("\n✨ Ready! Open your browser and start automating!")
    print("\n" + "="*60)
    
    try:
        # Import the Flask app
        from app import app
        
        # Run the application
        app.run(debug=False, host='0.0.0.0', port=5000)
        
    except ImportError as e:
        print(f"❌ Error importing Flask app: {e}")
        print("Make sure app.py is in the current directory")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n👋 Automation With Irtza stopped by user")
        print("Thank you for using Automation With Irtza!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")
        input("\nPress Enter to exit...")
        sys.exit(1)

if __name__ == '__main__':
    main()