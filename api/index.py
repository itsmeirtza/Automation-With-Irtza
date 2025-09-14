#!/usr/bin/env python3
"""
Vercel serverless function entry point for Automation With Irtza
"""
import sys
import os

# Add the parent directory to Python path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

# This is the handler that Vercel will call
def handler(request):
    return app(request.environ, lambda status, headers: None)

# For Vercel, we need to expose the app
application = app

if __name__ == "__main__":
    app.run(debug=True)