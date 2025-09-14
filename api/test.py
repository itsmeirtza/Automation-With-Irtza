#!/usr/bin/env python3
"""
Simple test function for Vercel deployment
"""
from flask import Flask, jsonify
import os
import sys

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({
        'message': 'Automation With Irtza - Test Deployment',
        'status': 'success',
        'platform': 'vercel',
        'python_version': sys.version,
        'env_vars': list(os.environ.keys())[:10]  # Show first 10 env vars
    })

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'service': 'automation-with-irtza'
    })

@app.route('/api/test')
def test_api():
    youtube_key = os.environ.get('YOUTUBE_API_KEY', 'NOT_SET')
    return jsonify({
        'api_test': 'passed',
        'youtube_api_configured': youtube_key != 'NOT_SET',
        'youtube_key_length': len(youtube_key) if youtube_key != 'NOT_SET' else 0
    })

# For Vercel
application = app

if __name__ == '__main__':
    app.run(debug=True)