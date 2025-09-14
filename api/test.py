from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    # Serve the main website HTML
    import os
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    website_path = os.path.join(parent_dir, 'website', 'index.html')
    
    try:
        with open(website_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return '''<!DOCTYPE html>
<html>
<head>
    <title>Automation With Irtza</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #0f0f23; color: #cccccc; text-align: center; }
        .error { background: #3a1a1a; padding: 20px; border-radius: 8px; border-left: 4px solid #ff4444; }
    </style>
</head>
<body>
    <div class="error">
        <h2>⚠️ Website Loading...</h2>
        <p>Original website files being loaded...</p>
        <a href="/test" style="color: #00ff88;">Test Page</a>
    </div>
</body>
</html>'''

# CSS and JS routes
@app.route('/css/<path:filename>')
def css_files(filename):
    import os
    from flask import send_from_directory
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return send_from_directory(os.path.join(parent_dir, 'website', 'css'), filename)

@app.route('/js/<path:filename>')
def js_files(filename):
    import os
    from flask import send_from_directory
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return send_from_directory(os.path.join(parent_dir, 'website', 'js'), filename)

@app.route('/test')
def test():
    return jsonify({
        'message': 'Automation With Irtza - API Test',
        'status': 'success',
        'platform': 'vercel',
        'author': 'Irtza Ali Waris',
        'email': 'irtzajutt2005@gmail.com'
    })

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'service': 'automation-with-irtza',
        'version': '1.0.0'
    })

# For Vercel
application = app
