#!/usr/bin/env python3
"""
Vercel serverless function entry point for Automation With Irtza
"""
import sys
import os
from pathlib import Path

# Add the parent directory to Python path to import our modules
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

try:
    # Import with error handling
    from app import app
    
    # Create necessary directories for Vercel environment
    os.makedirs('/tmp/videos/clips', exist_ok=True)
    os.makedirs('/tmp/videos/tmp', exist_ok=True)
    os.makedirs('/tmp/logs', exist_ok=True)
    
except ImportError as e:
    # Fallback Flask app if main app fails
    from flask import Flask, jsonify
    app = Flask(__name__)
    
    @app.route('/')
    def index():
        return jsonify({
            'error': 'Import failed',
            'message': str(e),
            'status': 'Vercel deployment needs debugging'
        })
    
    @app.route('/health')
    def health():
        return jsonify({'status': 'running', 'platform': 'vercel'})

except Exception as e:
    # Fallback for any other error
    from flask import Flask, jsonify
    app = Flask(__name__)
    
    @app.route('/')
    def index():
        return jsonify({
            'error': 'Startup failed',
            'message': str(e),
            'status': 'Vercel deployment error'
        })

# For Vercel, we need to expose the app
application = app

if __name__ == "__main__":
    app.run(debug=True)
