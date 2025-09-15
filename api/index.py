#!/usr/bin/env python3
"""
Vercel serverless function entry point for Automation With Irtza
Serves the complete Flask application with all routes and functionality
"""
import sys
import os
from pathlib import Path

# Add the parent directory to Python path to import our modules
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

try:
    # Try to import the main app
    from app import app
    print("✅ Successfully imported main Flask app")
    
    # Create necessary directories for Vercel serverless environment
    try:
        os.makedirs('/tmp/videos/clips', exist_ok=True)
        os.makedirs('/tmp/videos/tmp', exist_ok=True)
        os.makedirs('/tmp/logs', exist_ok=True)
    except:
        # If /tmp not available, use relative paths
        Path('videos/clips').mkdir(parents=True, exist_ok=True)
        Path('videos/tmp').mkdir(parents=True, exist_ok=True)
        Path('logs').mkdir(exist_ok=True)
    
except ImportError as e:
    print(f"❌ Import failed: {e}")
    # Create minimal Flask app if main app fails
    from flask import Flask, jsonify, send_from_directory
    app = Flask(__name__)
    
    @app.route('/')
    def index():
        # Try to serve the main website HTML directly
        try:
            website_path = os.path.join(parent_dir, 'website', 'index.html')
            with open(website_path, 'r', encoding='utf-8') as f:
                return f.read()
        except:
            return jsonify({
                'error': 'Could not load main app',
                'message': str(e),
                'solution': 'Check requirements.txt and dependencies'
            })
    
    @app.route('/css/<path:filename>')
    def css_files(filename):
        return send_from_directory(os.path.join(parent_dir, 'website', 'css'), filename)
    
    @app.route('/js/<path:filename>')
    def js_files(filename):
        return send_from_directory(os.path.join(parent_dir, 'website', 'js'), filename)
    
    @app.route('/health')
    def health():
        return jsonify({'status': 'fallback_mode', 'platform': 'vercel'})

except Exception as e:
    print(f"❌ Critical error: {e}")
    # Last resort fallback
    from flask import Flask, jsonify
    app = Flask(__name__)
    
    @app.route('/')
    def index():
        return jsonify({
            'error': 'Critical startup failure',
            'message': str(e),
            'platform': 'vercel'
        })

# For Vercel, we need to expose the app
application = app

if __name__ == "__main__":
    app.run(debug=True)
