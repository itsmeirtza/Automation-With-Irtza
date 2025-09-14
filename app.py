#!/usr/bin/env python3
"""
Automation With Irtza - Web Application Backend
Created by: Irtza Ali Waris
Email: Irtzaaliwaris@gmail.com
Website: https://ialiwaris.com

This Flask application provides the web interface for the video automation framework.
"""

import os
import json
import logging
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for
from werkzeug.utils import secure_filename
import threading
import time
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from urllib.parse import urlencode, urlparse
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
import re

# Import automation framework
from src.automation_framework import AutomationFramework
from src.config_manager import ConfigManager
from src.auto_clip_uploader import AutoClipUploader

app = Flask(__name__)
app.config['SECRET_KEY'] = 'automation-with-irtza-secret-key'
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create upload directory
Path(app.config['UPLOAD_FOLDER']).mkdir(exist_ok=True)

# Initialize automation framework
config_manager = ConfigManager()
automation_framework = AutomationFramework(config_manager)
clip_uploader = AutoClipUploader()

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

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@app.route('/')
def home():
    """Main homepage with 3D website"""
    return send_from_directory('website', 'index.html')

@app.route('/workflow')
def workflow():
    """Step-by-step workflow"""
    return render_template('workflow.html', state=workflow_state)

@app.route('/about')
def about():
    """About page"""
    return send_from_directory('website', 'about.html')

@app.route('/privacy')
def privacy():
    """Privacy policy page"""
    return send_from_directory('website', 'privacy.html')

@app.route('/terms')
def terms():
    """Terms of service page"""
    return send_from_directory('website', 'terms.html')

@app.route('/contact', methods=['POST'])
def contact():
    """Handle contact form submission"""
    try:
        data = request.get_json()
        name = data.get('name', '')
        email = data.get('email', '')
        company = data.get('company', '')
        message = data.get('message', '')
        
        if not name or not email or not message:
            return jsonify({'success': False, 'message': 'Please fill in all required fields'}), 400
        
        # Create email content
        email_subject = f"New Contact Form Submission from {name}"
        email_body = f"""
        New contact form submission from Automation With Irtza website:
        
        Name: {name}
        Email: {email}
        Company: {company if company else 'Not provided'}
        
        Message:
        {message}
        
        ---
        Sent from Automation With Irtza Contact Form
        Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        
        # For now, just log the email (in production you would send actual email)
        logger.info(f"Contact form submission: {email_subject}")
        logger.info(f"Content: {email_body}")
        
        # You can add actual email sending here using SMTP
        # send_email(email_subject, email_body, 'Irtzaaliwaris@gmail.com')
        
        return jsonify({'success': True, 'message': 'Thank you for your message! We will get back to you soon.'})
        
    except Exception as e:
        logger.error(f"Contact form error: {str(e)}")
        return jsonify({'success': False, 'message': 'An error occurred. Please try again later.'}), 500

@app.route('/dashboard')
def dashboard():
    """Dashboard view for monitoring all processes"""
    # Get system status
    system_status = {
        'active_tasks': 0,
        'clips_processed': len(workflow_state['clips']),
        'success_rate': 98.5,
        'uptime': '99.9%'
    }
    
    # Get recent activity
    recent_activity = [
        {'type': 'success', 'message': 'Video processing completed', 'time': '2 minutes ago'},
        {'type': 'upload', 'message': f"{len(workflow_state['clips'])} clips processed", 'time': '5 minutes ago'},
        {'type': 'info', 'message': 'AI transcription finished', 'time': '8 minutes ago'}
    ]
    
    return render_template('dashboard.html', 
                         system_status=system_status,
                         recent_activity=recent_activity,
                         clips=workflow_state['clips'])

@app.route('/api/set_youtube_channel', methods=['POST'])
def set_youtube_channel():
    """Step 1: Set YouTube channel link"""
    data = request.get_json()
    youtube_channel = data.get('channel_url', '').strip()
    
    if not youtube_channel:
        return jsonify({'success': False, 'message': 'YouTube channel URL is required'}), 400
    
    workflow_state['youtube_channel'] = youtube_channel
    workflow_state['current_step'] = 2
    workflow_state['error_message'] = ''
    
    logger.info(f"YouTube channel set: {youtube_channel}")
    return jsonify({'success': True, 'next_step': 2})

@app.route('/api/set_video_url', methods=['POST'])
def set_video_url():
    """Step 2: Set video URL for processing"""
    data = request.get_json()
    video_url = data.get('video_url', '').strip()
    
    if not video_url:
        return jsonify({'success': False, 'message': 'Video URL is required'}), 400
    
    workflow_state['video_url'] = video_url
    workflow_state['current_step'] = 3
    workflow_state['error_message'] = ''
    
    logger.info(f"Video URL set: {video_url}")
    return jsonify({'success': True, 'next_step': 3})

@app.route('/api/process_video', methods=['POST'])
def process_video():
    """Step 3: Process video and create clips"""
    if not workflow_state['video_url']:
        return jsonify({'success': False, 'message': 'No video URL provided'}), 400
    
    # Start processing in background
    workflow_state['processing_status'] = 'processing'
    workflow_state['progress'] = 0
    workflow_state['clips'] = []
    workflow_state['error_message'] = ''
    
    def process_in_background():
        try:
            logger.info("Starting video processing...")
            workflow_state['progress'] = 10
            
            # Process video with clip uploader
            results = clip_uploader.process_video(workflow_state['video_url'], dry_run=True)
            
            workflow_state['progress'] = 50
            logger.info(f"Processing results: {results}")
            
            # Update clips data
            workflow_state['clips'] = results.get('clips', [])[:6]  # Limit to 6 clips
            workflow_state['progress'] = 90
            
            if results.get('errors'):
                workflow_state['error_message'] = '; '.join(results['errors'])
                workflow_state['processing_status'] = 'error'
            else:
                workflow_state['processing_status'] = 'completed'
                workflow_state['current_step'] = 4
            
            workflow_state['progress'] = 100
            logger.info("Video processing completed")
            
        except Exception as e:
            logger.error(f"Video processing failed: {str(e)}")
            workflow_state['processing_status'] = 'error'
            workflow_state['error_message'] = str(e)
            workflow_state['progress'] = 0
    
    # Start background processing
    thread = threading.Thread(target=process_in_background)
    thread.daemon = True
    thread.start()
    
    return jsonify({'success': True, 'message': 'Video processing started'})

@app.route('/api/processing_status')
def processing_status():
    """Get current processing status"""
    return jsonify({
        'status': workflow_state['processing_status'],
        'progress': workflow_state['progress'],
        'clips_count': len(workflow_state['clips']),
        'error_message': workflow_state['error_message']
    })

@app.route('/api/get_clips')
def get_clips():
    """Step 4: Get preview of generated clips"""
    clips_data = []
    for i, clip in enumerate(workflow_state['clips']):
        clips_data.append({
            'id': i,
            'title': clip.get('title', f'Clip {i+1}'),
            'duration': f"{clip.get('duration', 0):.1f}s",
            'transcript': clip.get('transcript', '')[:100] + '...' if clip.get('transcript', '') else '',
            'file_path': clip.get('file_path', ''),
            'file_size': f"{clip.get('file_size', 0) / 1024 / 1024:.1f}MB" if clip.get('file_size') else '0MB'
        })
    
    return jsonify({
        'clips': clips_data,
        'total_clips': len(clips_data)
    })

@app.route('/api/upload_to_youtube', methods=['POST'])
def upload_to_youtube():
    """Step 5: Upload clips to YouTube (real upload if configured)"""
    data = request.get_json()
    selected_clips = data.get('selected_clips', list(range(len(workflow_state['clips']))))
    
    if not workflow_state['clips']:
        return jsonify({'success': False, 'message': 'No clips available for upload'}), 400
    
    # Start upload process
    workflow_state['processing_status'] = 'uploading'
    workflow_state['upload_results'] = {}
    
    def upload_in_background():
        try:
            logger.info("Starting YouTube upload...")
            youtube = None
            try:
                youtube = clip_uploader.youtube_auth()
            except Exception as e:
                logger.error(f"YouTube auth failed: {e}")
                workflow_state['error_message'] = f"YouTube auth failed: {e}"
                # We'll mark as error and stop
                workflow_state['processing_status'] = 'upload_error'
                return
            
            # Process each selected clip
            for clip_id in selected_clips:
                if clip_id < len(workflow_state['clips']):
                    clip = workflow_state['clips'][clip_id]
                    file_path = clip.get('file_path')
                    title = clip.get('title') or f"Clip {clip_id+1}"
                    description = clip.get('description') or ''
                    tags = clip.get('tags') or []
                    try:
                        resp = clip_uploader.youtube_upload(youtube, file_path, title, description, tags)
                        vid = resp.get('id') if isinstance(resp, dict) else None
                        workflow_state['upload_results'][clip_id] = {
                            'success': True,
                            'youtube_id': vid or 'unknown',
                            'url': f'https://youtube.com/watch?v={vid}' if vid else ''
                        }
                        logger.info(f"Uploaded clip {clip_id} -> {vid}")
                    except Exception as e:
                        err = f"Upload failed for clip {clip_id}: {e}"
                        logger.error(err)
                        workflow_state['upload_results'][clip_id] = {
                            'success': False,
                            'error': str(e)
                        }
            
            workflow_state['processing_status'] = 'upload_completed'
            workflow_state['current_step'] = 6
            logger.info("YouTube upload completed")
            
        except Exception as e:
            logger.error(f"YouTube upload failed: {str(e)}")
            workflow_state['processing_status'] = 'upload_error'
            workflow_state['error_message'] = str(e)
    
    # Start background upload
    thread = threading.Thread(target=upload_in_background)
    thread.daemon = True
    thread.start()
    
    return jsonify({'success': True, 'message': 'YouTube upload started'})

@app.route('/api/upload_status')
def upload_status():
    """Get upload status"""
    return jsonify({
        'status': workflow_state['processing_status'],
        'results': workflow_state['upload_results'],
        'error_message': workflow_state['error_message']
    })

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
    return jsonify({'success': True})

@app.route('/static/<path:filename>')
def static_files(filename):
    """Serve static files"""
    return send_from_directory('website', filename)

@app.route('/css/<path:filename>')
def css_files(filename):
    """Serve CSS files"""
    return send_from_directory('website/css', filename)

@app.route('/js/<path:filename>')
def js_files(filename):
    """Serve JS files"""
    return send_from_directory('website/js', filename)

@app.route('/videos/<path:filename>')
def video_files(filename):
    """Serve video files"""
    return send_from_directory('videos', filename)

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500

# ----------------------------
# YouTube Data API integration
# ----------------------------

def get_youtube_api_key():
    return os.environ.get('YOUTUBE_API_KEY')

def _http_get_json(url: str):
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0 (AutomationWithIrtza/1.0)'} )
        with urlopen(req, timeout=10) as resp:
            data = resp.read().decode('utf-8')
            return json.loads(data)
    except (HTTPError, URLError, TimeoutError) as e:
        logger.error(f"YouTube API HTTP error: {e}")
        return None
    except Exception as e:
        logger.error(f"YouTube API parse error: {e}")
        return None

def parse_channel_id_from_url(channel_url: str):
    """Best-effort parse of channel ID. Supports /channel/ID and @handle and /user/NAME.
    For @handle and user, falls back to search API to resolve channelId."""
    if not channel_url:
        return None

    try:
        # Extract after youtube.com/
        if 'channel/' in channel_url:
            return channel_url.split('channel/')[1].split('/')[0]
        if '@' in channel_url:
            handle = channel_url.split('@')[1].split('/')[0]
            return resolve_channel_id_by_search(handle)
        if '/user/' in channel_url:
            username = channel_url.split('/user/')[1].split('/')[0]
            # Try forUsername first (legacy)
            api_key = get_youtube_api_key()
            if not api_key:
                return None
            url = 'https://www.googleapis.com/youtube/v3/channels?' + urlencode({
                'part': 'id',
                'forUsername': username,
                'key': api_key
            })
            data = _http_get_json(url)
            if data and data.get('items'):
                return data['items'][0]['id']
            # Fallback to search
            return resolve_channel_id_by_search(username)
    except Exception:
        pass
    
    # As last resort, try to use the URL path as query
    path = urlparse(channel_url).path.strip('/')
    if path:
        return resolve_channel_id_by_search(path.replace('@',''))
    return None

def resolve_channel_id_by_search(query: str):
    api_key = get_youtube_api_key()
    if not api_key:
        return None
    url = 'https://www.googleapis.com/youtube/v3/search?' + urlencode({
        'part': 'snippet',
        'type': 'channel',
        'q': query,
        'maxResults': 1,
        'key': api_key
    })
    data = _http_get_json(url)
    if data and data.get('items'):
        return data['items'][0]['snippet']['channelId'] if 'channelId' in data['items'][0]['snippet'] else data['items'][0]['id'].get('channelId')
    return None

def parse_iso8601_duration(duration: str) -> float:
    """Parse ISO8601 duration like PT1M5S to seconds."""
    if not duration or not duration.startswith('P'):
        return 0.0
    hours = minutes = seconds = 0
    match_h = re.search(r"(\d+)H", duration)
    match_m = re.search(r"(\d+)M", duration)
    match_s = re.search(r"(\d+)S", duration)
    if match_h:
        hours = int(match_h.group(1))
    if match_m:
        minutes = int(match_m.group(1))
    if match_s:
        seconds = int(match_s.group(1))
    return hours*3600 + minutes*60 + seconds

@app.route('/api/youtube/channel_info')
def api_youtube_channel_info():
    channel_url = request.args.get('channel_url', '')
    api_key = get_youtube_api_key()
    if not api_key:
        return jsonify({'success': False, 'message': 'Server is missing YOUTUBE_API_KEY'}), 500
    channel_id = parse_channel_id_from_url(channel_url)
    if not channel_id:
        return jsonify({'success': False, 'message': 'Unable to resolve channel from URL'}), 400
    url = 'https://www.googleapis.com/youtube/v3/channels?' + urlencode({
        'part': 'snippet,statistics',
        'id': channel_id,
        'key': api_key
    })
    data = _http_get_json(url)
    if not data or not data.get('items'):
        return jsonify({'success': False, 'message': 'No data returned from YouTube'}), 502
    item = data['items'][0]
    snippet = item.get('snippet', {})
    statistics = item.get('statistics', {})
    return jsonify({
        'success': True,
        'channelId': channel_id,
        'title': snippet.get('title'),
        'description': snippet.get('description'),
        'customUrl': snippet.get('customUrl'),
        'thumbnails': snippet.get('thumbnails', {}),
        'statistics': statistics
    })

@app.route('/api/youtube/latest_videos')
def api_youtube_latest_videos():
    channel_url = request.args.get('channel_url', '')
    api_key = get_youtube_api_key()
    if not api_key:
        return jsonify({'success': False, 'message': 'Server is missing YOUTUBE_API_KEY'}), 500
    channel_id = parse_channel_id_from_url(channel_url)
    if not channel_id:
        return jsonify({'success': False, 'message': 'Unable to resolve channel from URL'}), 400

    # Step 1: get latest video IDs from the channel
    search_url = 'https://www.googleapis.com/youtube/v3/search?' + urlencode({
        'part': 'snippet',
        'channelId': channel_id,
        'order': 'date',
        'type': 'video',
        'maxResults': 15,
        'key': api_key
    })
    search_data = _http_get_json(search_url)
    if not search_data:
        return jsonify({'success': False, 'message': 'Search failed'}), 502

    items = search_data.get('items', [])
    video_ids = []
    snippet_map = {}
    for it in items:
        vid = it.get('id', {}).get('videoId')
        sn = it.get('snippet', {})
        if vid:
            video_ids.append(vid)
            snippet_map[vid] = sn

    if not video_ids:
        return jsonify({'success': True, 'videos': []})

    # Step 2: get durations and more details
    videos_url = 'https://www.googleapis.com/youtube/v3/videos?' + urlencode({
        'part': 'contentDetails,snippet',
        'id': ','.join(video_ids),
        'key': api_key
    })
    videos_data = _http_get_json(videos_url)
    if not videos_data:
        return jsonify({'success': False, 'message': 'Videos fetch failed'}), 502

    videos = []
    for item in videos_data.get('items', []):
        vid = item.get('id')
        sn = item.get('snippet', {})
        cd = item.get('contentDetails', {})
        duration_s = parse_iso8601_duration(cd.get('duration',''))
        # Treat as short if <= 90 seconds
        is_short = duration_s <= 90
        thumb = None
        thumbs = sn.get('thumbnails', {})
        # pick best available
        for key in ['medium','high','default']:
            if key in thumbs:
                thumb = thumbs[key]['url']
                break
        videos.append({
            'id': vid,
            'title': sn.get('title') or (snippet_map.get(vid, {}).get('title')),
            'publishedAt': sn.get('publishedAt') or (snippet_map.get(vid, {}).get('publishedAt')),
            'thumbnail': thumb,
            'durationSeconds': duration_s,
            'isShort': is_short
        })

    # Prioritize shorts at the top
    videos.sort(key=lambda v: (not v['isShort'], v.get('publishedAt','')), reverse=False)
    return jsonify({'success': True, 'videos': videos})

if __name__ == '__main__':
    logger.info("Starting Automation With Irtza web application...")
    logger.info("Created by: Irtza Ali Waris")
    logger.info("Email: Irtzaaliwaris@gmail.com")
    logger.info("Website: https://ialiwaris.com")
    
    # Create necessary directories
    Path('videos/clips').mkdir(parents=True, exist_ok=True)
    Path('videos/tmp').mkdir(parents=True, exist_ok=True)
    Path('logs').mkdir(exist_ok=True)
    
    # Run the application
    app.run(debug=True, host='0.0.0.0', port=5000)