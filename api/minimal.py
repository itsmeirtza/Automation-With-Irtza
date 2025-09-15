from flask import Flask, send_from_directory
import os

app = Flask(__name__)

# Get parent directory path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@app.route('/')
def index():
    """Serve main website"""
    try:
        return send_from_directory(os.path.join(parent_dir, 'website'), 'index.html')
    except Exception as e:
        return f'''<!DOCTYPE html>
<html>
<head>
    <title>Automation With Irtza</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background: #0f0f23; color: #cccccc; text-align: center; }}
        .container {{ max-width: 600px; margin: 0 auto; }}
        .logo {{ font-size: 2em; color: #00ff88; margin-bottom: 20px; }}
        .error {{ background: #3a1a1a; padding: 20px; border-radius: 8px; border-left: 4px solid #ff4444; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">🤖 Automation With Irtza</div>
        <div class="error">
            <h2>⚡ Loading Website...</h2>
            <p>Website is starting up...</p>
            <p><small>Error: {str(e)}</small></p>
        </div>
    </div>
</body>
</html>'''

@app.route('/css/<path:filename>')
def serve_css(filename):
    """Serve CSS files"""
    return send_from_directory(os.path.join(parent_dir, 'website', 'css'), filename)

@app.route('/js/<path:filename>')
def serve_js(filename):
    """Serve JS files"""
    return send_from_directory(os.path.join(parent_dir, 'website', 'js'), filename)

@app.route('/images/<path:filename>')
def serve_images(filename):
    """Serve image files"""
    return send_from_directory(os.path.join(parent_dir, 'website', 'images'), filename)

@app.route('/about')
def about():
    """Serve about page"""
    return send_from_directory(os.path.join(parent_dir, 'website'), 'about.html')

@app.route('/privacy')
def privacy():
    """Serve privacy page"""
    return send_from_directory(os.path.join(parent_dir, 'website'), 'privacy.html')

@app.route('/terms')
def terms():
    """Serve terms page"""
    return send_from_directory(os.path.join(parent_dir, 'website'), 'terms.html')

@app.route('/health')
def health():
    """Health check"""
    return {'status': 'healthy', 'service': 'automation-with-irtza', 'version': '1.0.0'}

# For Vercel
application = app