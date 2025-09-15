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

@app.route('/api/set_video_url', methods=['POST'])
def set_video_url():
    """Set video URL for processing"""
    try:
        from flask import request, jsonify
        data = request.get_json()
        video_url = data.get('video_url', '').strip() if data else ''
        
        if not video_url:
            return jsonify({'success': False, 'message': 'Video URL is required'}), 400
        
        # For now, just return success (later we'll add actual processing)
        return jsonify({
            'success': True, 
            'message': 'Video URL set successfully',
            'video_url': video_url,
            'next_step': 3
        })
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@app.route('/api/process_video', methods=['POST'])
def process_video():
    """Process video and create clips (mock implementation)"""
    try:
        from flask import jsonify
        # Mock successful processing
        return jsonify({
            'success': True,
            'message': 'Video processing started',
            'status': 'processing',
            'clips_generated': 6
        })
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@app.route('/api/get_clips')
def get_clips():
    """Get processed clips (mock data)"""
    try:
        from flask import jsonify
        # Mock clip data
        clips = [
            {'id': 1, 'title': 'Clip 1', 'duration': '30s', 'thumbnail': '/images/clip1.jpg'},
            {'id': 2, 'title': 'Clip 2', 'duration': '45s', 'thumbnail': '/images/clip2.jpg'},
            {'id': 3, 'title': 'Clip 3', 'duration': '60s', 'thumbnail': '/images/clip3.jpg'}
        ]
        return jsonify({'success': True, 'clips': clips, 'total_clips': len(clips)})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@app.route('/workflow')
def workflow():
    """Serve workflow page"""
    try:
        return send_from_directory(os.path.join(parent_dir, 'templates'), 'workflow.html')
    except:
        # Fallback if templates not found
        return send_from_directory(os.path.join(parent_dir, 'website'), 'index.html')

@app.route('/dashboard')
def dashboard():
    """Serve dashboard page"""
    try:
        return send_from_directory(os.path.join(parent_dir, 'templates'), 'dashboard.html')
    except:
        return send_from_directory(os.path.join(parent_dir, 'website'), 'index.html')

@app.route('/health')
def health():
    """Health check"""
    return {'status': 'healthy', 'service': 'automation-with-irtza', 'version': '1.0.0'}

# For Vercel
application = app
