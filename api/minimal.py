from flask import Flask, send_from_directory, request, jsonify
import os
import json
import time
import re
import random
from datetime import datetime
from urllib.parse import urlparse, parse_qs

app = Flask(__name__)

# Get parent directory path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Global state for workflow
workflow_state = {
    'current_step': 1,
    'youtube_channel': '',
    'video_url': '',
    'processing_status': 'idle',
    'clips': [],
    'progress': 0,
    'error_message': '',
    'upload_results': {}
}

# Mock video data for testing
mock_videos = [
    {'id': 'QPO6PfTdYrI', 'title': 'itsmeirtza Channel Content', 'duration': 300, 'views': '1.2K'},
    {'id': 'dQw4w9WgXcQ', 'title': 'Amazing Tutorial Video', 'duration': 450, 'views': '890K'},
    {'id': 'kJQP7kiw5Fk', 'title': 'How to Build Apps', 'duration': 600, 'views': '2.1M'}
]

# Channel data
channel_data = {
    '@itsmeirtza': {
        'id': 'UCitsmeirtza123',
        'name': 'itsmeirtza',
        'subscribers': '1.2K',
        'videos': 25,
        'description': 'Tech content creator and automation specialist'
    }
}

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

# Helper functions
def extract_video_id(url):
    """Extract YouTube video ID from URL"""
    patterns = [
        r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([\w-]+)',
        r'youtube\.com/watch\?.*v=([\w-]+)'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def generate_metadata(transcript, video_title=""):
    """Generate SEO-optimized metadata"""
    # Extract keywords from transcript
    words = re.findall(r'\w+', transcript.lower())
    common_words = ['the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were']
    keywords = [w for w in words if len(w) > 3 and w not in common_words]
    
    # Generate title
    if len(keywords) >= 3:
        title = f"{keywords[0].title()} {keywords[1].title()} - {keywords[2].title()} Guide"
    else:
        title = f"Amazing {video_title} Clip"
    
    # Generate description
    description = f"""🎯 {title}
    
📌 Key Topics Covered:
• {keywords[0].title() if keywords else 'Tutorial'}
• {keywords[1].title() if len(keywords) > 1 else 'Tips'}
• {keywords[2].title() if len(keywords) > 2 else 'Techniques'}

🚀 Created by: Automation With Irtza
🌐 Website: https://teamirtza.online
📧 Contact: irtzajutt2005@gmail.com

#AutomationWithIrtza #Tutorial #Tips #Learning"""
    
    # Generate tags
    base_tags = ['automation', 'tutorial', 'tips', 'guide', 'learning']
    content_tags = keywords[:10] if keywords else []
    seo_tags = ['howto', 'stepbystep', 'beginner', 'advanced', 'tricks']
    
    all_tags = base_tags + content_tags + seo_tags
    return title[:100], description[:5000], all_tags[:50]

# API Routes
@app.route('/api/set_youtube_channel', methods=['POST'])
def set_youtube_channel():
    """Step 1: Set YouTube channel"""
    try:
        data = request.get_json()
        channel_url = data.get('channel_url', '').strip() if data else ''
        
        if not channel_url:
            return jsonify({'success': False, 'message': 'YouTube channel URL is required'}), 400
        
        workflow_state['youtube_channel'] = channel_url
        workflow_state['current_step'] = 2
        workflow_state['error_message'] = ''
        
        return jsonify({
            'success': True,
            'message': 'YouTube channel set successfully',
            'channel_url': channel_url,
            'next_step': 2
        })
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@app.route('/api/set_video_url', methods=['POST'])
def set_video_url():
    """Step 2: Set video URL for processing"""
    try:
        data = request.get_json()
        video_url = data.get('video_url', '').strip() if data else ''
        
        if not video_url:
            return jsonify({'success': False, 'message': 'Video URL is required'}), 400
        
        video_id = extract_video_id(video_url)
        if not video_id:
            return jsonify({'success': False, 'message': 'Invalid YouTube URL'}), 400
        
        workflow_state['video_url'] = video_url
        workflow_state['current_step'] = 3
        workflow_state['error_message'] = ''
        
        return jsonify({
            'success': True, 
            'message': 'Video URL set successfully',
            'video_url': video_url,
            'video_id': video_id,
            'next_step': 3
        })
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@app.route('/api/process_video', methods=['POST'])
def process_video():
    """Step 3: Process video and create clips with AI metadata"""
    try:
        if not workflow_state['video_url']:
            return jsonify({'success': False, 'message': 'No video URL provided'}), 400
        
        video_id = extract_video_id(workflow_state['video_url'])
        if not video_id:
            return jsonify({'success': False, 'message': 'Invalid video URL'}), 400
        
        # Start processing
        workflow_state['processing_status'] = 'processing'
        workflow_state['progress'] = 0
        workflow_state['clips'] = []
        workflow_state['error_message'] = ''
        
        # Simulate processing steps
        processing_steps = [
            {'step': 'Analyzing video...', 'progress': 10},
            {'step': 'Detecting scenes...', 'progress': 30},
            {'step': 'Creating clips...', 'progress': 50},
            {'step': 'Generating transcripts...', 'progress': 70},
            {'step': 'Creating metadata...', 'progress': 90},
            {'step': 'Finalizing...', 'progress': 100}
        ]
        
        # Generate mock clips with AI metadata based on your video
        # Video ID: QPO6PfTdYrI from @itsmeirtza
        mock_transcripts = [
            "Welcome to itsmeirtza channel where we explore amazing tech content and automation",
            "Learn the latest programming techniques and development best practices with irtza",
            "Discover powerful automation tools that will streamline your workflow process",
            "Master advanced coding concepts and build scalable applications efficiently",
            "Explore cutting-edge technologies and innovative solutions for developers",
            "Implement robust testing strategies and deployment techniques for production"
        ]
        
        clips = []
        for i in range(6):
            transcript = mock_transcripts[i] if i < len(mock_transcripts) else f"Amazing tutorial content about development topic {i+1}"
            title, description, tags = generate_metadata(transcript, f"Tutorial {i+1}")
            
            clip = {
                'id': i + 1,
                'title': title,
                'description': description,
                'tags': tags,
                'duration': f"{random.randint(30, 120)}s",
                'transcript': transcript,
                'thumbnail': f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg",
                'preview_url': f"https://www.youtube.com/embed/{video_id}?start={i*60}&end={(i+1)*60}",
                'file_size': f"{random.randint(5, 25)} MB",
                'quality': 'HD 1080p',
                'uploaded': False,
                'seo_score': random.randint(85, 98)
            }
            clips.append(clip)
        
        workflow_state['clips'] = clips
        workflow_state['processing_status'] = 'completed'
        workflow_state['current_step'] = 4
        workflow_state['progress'] = 100
        
        return jsonify({
            'success': True,
            'message': 'Video processing completed successfully',
            'status': 'completed',
            'clips_generated': len(clips),
            'clips': clips,
            'next_step': 4
        })
    except Exception as e:
        workflow_state['processing_status'] = 'error'
        workflow_state['error_message'] = str(e)
        return jsonify({'success': False, 'message': f'Processing failed: {str(e)}'}), 500

@app.route('/api/get_clips')
def get_clips():
    """Get processed clips with previews"""
    try:
        clips = workflow_state['clips']
        return jsonify({
            'success': True, 
            'clips': clips, 
            'total_clips': len(clips),
            'processing_status': workflow_state['processing_status'],
            'progress': workflow_state['progress']
        })
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@app.route('/api/upload_to_youtube', methods=['POST'])
def upload_to_youtube():
    """Step 4: Upload selected clips to YouTube"""
    try:
        data = request.get_json()
        selected_clips = data.get('selected_clips', list(range(len(workflow_state['clips']))))
        
        if not workflow_state['clips']:
            return jsonify({'success': False, 'message': 'No clips available for upload'}), 400
        
        workflow_state['processing_status'] = 'uploading'
        workflow_state['upload_results'] = {}
        
        # Simulate upload process
        upload_results = {}
        for clip_id in selected_clips:
            if clip_id < len(workflow_state['clips']):
                clip = workflow_state['clips'][clip_id]
                
                # Simulate upload success/failure (95% success rate)
                success = random.random() > 0.05
                
                if success:
                    video_id = f"mock_vid_{random.randint(100000, 999999)}"
                    upload_results[clip_id] = {
                        'success': True,
                        'youtube_id': video_id,
                        'url': f'https://youtube.com/watch?v={video_id}',
                        'title': clip['title'],
                        'upload_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'views': 0,
                        'status': 'published'
                    }
                    # Mark clip as uploaded
                    workflow_state['clips'][clip_id]['uploaded'] = True
                    workflow_state['clips'][clip_id]['youtube_url'] = f'https://youtube.com/watch?v={video_id}'
                else:
                    upload_results[clip_id] = {
                        'success': False,
                        'error': 'Upload quota exceeded. Try again later.',
                        'title': clip['title']
                    }
        
        workflow_state['upload_results'] = upload_results
        workflow_state['processing_status'] = 'upload_completed'
        
        successful_uploads = len([r for r in upload_results.values() if r['success']])
        
        return jsonify({
            'success': True,
            'message': f'Upload completed: {successful_uploads}/{len(selected_clips)} clips uploaded successfully',
            'upload_results': upload_results,
            'successful_uploads': successful_uploads,
            'total_clips': len(selected_clips)
        })
    except Exception as e:
        workflow_state['processing_status'] = 'upload_error'
        workflow_state['error_message'] = str(e)
        return jsonify({'success': False, 'message': f'Upload failed: {str(e)}'}), 500

@app.route('/api/workflow_state')
def get_workflow_state():
    """Get complete workflow state"""
    return jsonify(workflow_state)

@app.route('/api/reset_workflow', methods=['POST'])
def reset_workflow():
    """Reset workflow to start over"""
    global workflow_state
    workflow_state = {
        'current_step': 1,
        'youtube_channel': '',
        'video_url': '',
        'processing_status': 'idle',
        'clips': [],
        'progress': 0,
        'error_message': '',
        'upload_results': {}
    }
        return jsonify({'success': True, 'message': 'Workflow reset successfully'})

@app.route('/api/channel_info')
def get_channel_info():
    """Get channel information"""
    try:
        channel_url = request.args.get('channel', '')
        if '@itsmeirtza' in channel_url or 'itsmeirtza' in channel_url:
            return jsonify({
                'success': True,
                'channel': channel_data['@itsmeirtza'],
                'recent_videos': [
                    {
                        'id': 'QPO6PfTdYrI',
                        'title': 'Latest Video from itsmeirtza',
                        'views': '1.2K',
                        'duration': '5:30',
                        'upload_date': '2 days ago'
                    }
                ]
            })
        else:
            return jsonify({
                'success': True,
                'channel': {'name': 'Channel', 'subscribers': 'N/A'},
                'recent_videos': []
            })
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@app.route('/api/preview_clip/<int:clip_id>')
def preview_clip(clip_id):
    """Get preview data for a specific clip"""
    try:
        if clip_id < len(workflow_state['clips']):
            clip = workflow_state['clips'][clip_id]
            return jsonify({
                'success': True,
                'clip': clip,
                'preview_available': True
            })
        else:
            return jsonify({'success': False, 'message': 'Clip not found'}), 404
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

@app.route('/api/test')
def api_test():
    """Test API endpoint"""
    return jsonify({
        'status': 'working',
        'message': 'API is working perfectly!',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'workflow_state': workflow_state,
        'available_endpoints': [
            '/api/set_youtube_channel',
            '/api/set_video_url', 
            '/api/process_video',
            '/api/get_clips',
            '/api/upload_to_youtube'
        ]
    })

@app.route('/debug')
def debug_page():
    """Debug page to check system status"""
    return f'''<!DOCTYPE html>
<html>
<head>
    <title>Debug - Automation With Irtza</title>
    <style>
        body {{ font-family: monospace; background: #1a1a1a; color: #00ff88; padding: 20px; }}
        .status {{ background: #2a2a2a; padding: 15px; margin: 10px 0; border-radius: 5px; }}
        .working {{ border-left: 4px solid #00ff88; }}
        pre {{ background: #0a0a0a; padding: 15px; border-radius: 5px; overflow-x: auto; }}
        .btn {{ background: #00ff88; color: #1a1a1a; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin: 5px; }}
    </style>
</head>
<body>
    <h1>🔧 Automation With Irtza - Debug Panel</h1>
    
    <div class="status working">
        <h3>✅ System Status: ONLINE</h3>
        <p>Flask App: Working</p>
        <p>Current Time: {datetime.now()}</p>
        <p>Workflow Step: {workflow_state['current_step']}</p>
    </div>
    
    <div class="status working">
        <h3>📊 Current Workflow State:</h3>
        <pre>{json.dumps(workflow_state, indent=2)}</pre>
    </div>
    
    <div class="status working">
        <h3>🧪 Quick Tests:</h3>
        <button class="btn" onclick="testAPI()">Test API</button>
        <button class="btn" onclick="testWorkflow()">Test Workflow</button>
        <button class="btn" onclick="resetWorkflow()">Reset</button>
        <div id="test-results" style="margin-top: 20px;"></div>
    </div>
    
    <script>
        async function testAPI() {{
            const response = await fetch('/api/test');
            const data = await response.json();
            document.getElementById('test-results').innerHTML = 
                '<pre style="color: #00ff88;">API Test Result:\n' + JSON.stringify(data, null, 2) + '</pre>';
        }}
        
        async function testWorkflow() {{
            const response = await fetch('/api/set_video_url', {{
                method: 'POST',
                headers: {{'Content-Type': 'application/json'}},
                body: JSON.stringify({{'video_url': 'https://youtube.com/watch?v=test123'}})
            }});
            const data = await response.json();
            document.getElementById('test-results').innerHTML = 
                '<pre style="color: #ffaa00;">Workflow Test Result:\n' + JSON.stringify(data, null, 2) + '</pre>';
        }}
        
        async function resetWorkflow() {{
            const response = await fetch('/api/reset_workflow', {{
                method: 'POST'
            }});
            const data = await response.json();
            document.getElementById('test-results').innerHTML = 
                '<pre style="color: #ff4400;">Reset Result:\n' + JSON.stringify(data, null, 2) + '</pre>';
            setTimeout(() => location.reload(), 1000);
        }}
    </script>
</body>
</html>'''

# For Vercel
application = app
