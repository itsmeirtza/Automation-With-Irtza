from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return '''<!DOCTYPE html>
<html>
<head>
    <title>Automation With Irtza</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #0f0f23; color: #cccccc; }
        .container { max-width: 600px; margin: 0 auto; text-align: center; }
        .logo { font-size: 2em; color: #00ff88; margin-bottom: 20px; }
        .status { background: #1a1a3a; padding: 20px; border-radius: 8px; margin: 20px 0; }
        .success { border-left: 4px solid #00ff88; }
        a { color: #00ff88; text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">🤖 Automation With Irtza</div>
        <div class="status success">
            <h2>✅ Deployment Successful!</h2>
            <p>Your automation framework is running on Vercel</p>
            <p><strong>Created by:</strong> Irtza Ali Waris</p>
            <p><strong>Email:</strong> irtzajutt2005@gmail.com</p>
        </div>
        <div style="margin: 30px 0;">
            <a href="/test">[API Test]</a> • 
            <a href="/health">[Health Check]</a> • 
            <a href="/website/">[Website]</a>
        </div>
        <p style="color: #666; font-size: 0.9em;">Platform: Vercel Serverless Functions</p>
    </div>
</body>
</html>'''

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
