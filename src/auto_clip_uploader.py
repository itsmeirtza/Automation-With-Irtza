"""
Auto Clip Uploader (free-stack)

This script:
 - Detects scene-change timestamps from a remote video URL (no full download)
 - Extracts short clips (ffmpeg streaming, no full download)
 - Transcribes clips with OpenAI's whisper (local models - free)
 - Generates titles/descriptions/tags using simple TF-IDF heuristics (free)
 - Uploads up to 6 clips/day to YouTube using YouTube Data API (free but needs OAuth client_secret.json)

Important notes BEFORE running:
 - You must have `ffmpeg` installed and on PATH.
 - Install Python packages from requirements.txt.
 - Put your YouTube OAuth client JSON as `client_secret.json` in same folder.
 - First run will open a browser to authorize your channel (you must do that once interactively).
 - Whisper will download model weights (free) the first time; choose tiny/small for speed.
 - This is intended as an MVP: add manual review step for safety/copyright before fully automatic posting.
"""

import os
import re
import sys
import math
import json
import time
import pickle
import shutil
import string
import subprocess
import logging
from pathlib import Path
from collections import Counter
from typing import List, Tuple, Dict, Any, Optional

# 3rd-party libs (optional imports for graceful degradation)
try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False
    whisper = None

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    TfidfVectorizer = None

try:
    from googleapiclient.discovery import build
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.http import MediaFileUpload
    YOUTUBE_API_AVAILABLE = True
except ImportError:
    YOUTUBE_API_AVAILABLE = False


class AutoClipUploader:
    """Auto Clip Uploader class for automation framework integration."""
    
    # Configuration constants
    SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
    CLIP_DIR = Path("videos/clips")
    TMP_DIR = Path("videos/tmp")
    MAX_CLIPS_PER_RUN = 6
    WHISPER_MODEL = "tiny"
    SCENE_THRESHOLD = 0.4
    MIN_CLIP_SECONDS = 5
    MAX_CLIP_SECONDS = 180
    
    def __init__(self):
        """Initialize the Auto Clip Uploader."""
        self.logger = logging.getLogger(__name__)
        self._check_dependencies()
    
    def _check_dependencies(self) -> None:
        """Check if required dependencies are available."""
        missing_deps = []
        
        if not WHISPER_AVAILABLE:
            missing_deps.append("whisper")
        if not SKLEARN_AVAILABLE:
            missing_deps.append("scikit-learn")
        if not YOUTUBE_API_AVAILABLE:
            missing_deps.append("google-api-python-client, google-auth-oauthlib, google-auth-httplib2")
        
        # Check ffmpeg
        try:
            subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            missing_deps.append("ffmpeg (must be installed and on PATH)")
        
        if missing_deps:
            self.logger.error(f"Missing dependencies: {', '.join(missing_deps)}")
            self.logger.error("Run: pip install whisper scikit-learn google-api-python-client google-auth-oauthlib google-auth-httplib2")
    
    def youtube_auth(self) -> Any:
        """OAuth flow. Requires client_secret.json in working dir."""
        if not YOUTUBE_API_AVAILABLE:
            raise RuntimeError("YouTube API libraries not available")
        
        creds = None
        token_file = Path("token.pkl")
        if token_file.exists():
            with token_file.open("rb") as f:
                creds = pickle.load(f)
        if not creds or not getattr(creds, "valid", False):
            if creds and getattr(creds, "expired", False) and getattr(creds, "refresh_token", None):
                creds.refresh(Request())
            else:
                if not Path("client_secret.json").exists():
                    raise RuntimeError("client_secret.json missing. Create a Google Cloud OAuth client and save as client_secret.json")
                flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", self.SCOPES)
                creds = flow.run_local_server(port=0)
            with token_file.open("wb") as f:
                pickle.dump(creds, f)
        return build("youtube", "v3", credentials=creds)
    
    def youtube_upload(self, youtube: Any, file_path: str, title: str, description: str, tags: List[str]) -> Dict:
        """Upload video to YouTube."""
        if not YOUTUBE_API_AVAILABLE:
            raise RuntimeError("YouTube API libraries not available")
        
        media = MediaFileUpload(file_path, chunksize=-1, resumable=True)
        body = {
            'snippet': {
                'title': title[:100],
                'description': description,
                'tags': tags[:50],
                'categoryId': '22',
            },
            'status': {
                'privacyStatus': 'public'
            }
        }
        req = youtube.videos().insert(part='snippet,status', body=body, media_body=media)
        resp = None
        while resp is None:
            status, resp = req.next_chunk()
            if status:
                self.logger.info(f"Upload progress {int(status.progress() * 100)}%")
        self.logger.info(f"Upload finished, video id: {resp.get('id')}")
        return resp
    
    def prepare_input(self, url: str) -> str:
        """Prepare an input source for ffmpeg.
        - If the url is a YouTube link, try to download using yt-dlp to a temp file and return its path.
        - Otherwise return the original URL/path.
        """
        if 'youtube.com' in url or 'youtu.be' in url:
            self.logger.info("Detected YouTube URL; attempting to fetch with yt-dlp")
            self.TMP_DIR.mkdir(parents=True, exist_ok=True)
            out_tpl = str(self.TMP_DIR / 'source.%(ext)s')
            try:
                subprocess.run(['yt-dlp', '-f', 'mp4', '-o', out_tpl, url], check=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                # Try with best format if mp4 not available or yt-dlp missing
                try:
                    subprocess.run(['yt-dlp', '-o', out_tpl, url], check=True)
                except Exception as e:
                    self.logger.error(f"yt-dlp failed or not installed: {e}")
                    raise RuntimeError("yt-dlp is required to process YouTube URLs. Install with: pip install yt-dlp")
            # Find the downloaded file
            for ext in ['mp4', 'mkv', 'webm']:
                candidate = self.TMP_DIR / f'source.{ext}'
                if candidate.exists():
                    self.logger.info(f"Using downloaded file: {candidate}")
                    return str(candidate)
            # Fallback: pick the newest file in TMP_DIR
            files = list(self.TMP_DIR.glob('source.*'))
            if files:
                latest = max(files, key=lambda p: p.stat().st_mtime)
                self.logger.info(f"Using downloaded file: {latest}")
                return str(latest)
            raise RuntimeError("Failed to locate downloaded video file from yt-dlp")
        return url

    def run_ffmpeg_scene_detect(self, input_url: str, scene_threshold: float = None) -> List[float]:
        """
        Use ffmpeg's scene detection filter to produce timestamps where scene changes occur.
        Works with both local files and remote URLs.
        Returns list of timestamps (seconds) where scenes were detected.
        """
        if scene_threshold is None:
            scene_threshold = self.SCENE_THRESHOLD
        
        cmd = [
            "ffmpeg",
            "-hide_banner",
            "-loglevel", "info",
            "-i", input_url,
            "-vf", f"select=gt(scene\\,{scene_threshold}),showinfo",
            "-f", "null", "-"
        ]
        self.logger.info("Running ffmpeg for scene detection (may take a while)")
        self.logger.debug(f"Command: {' '.join(cmd)}")
        
        proc = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        scene_pts = []
        
        for line in proc.stderr:
            m = re.search(r"pts_time:(?P<pts>[0-9]+\.?[0-9]*)", line)
            if m:
                t = float(m.group('pts'))
                scene_pts.append(t)
        
        proc.wait()
        self.logger.info(f"Detected {len(scene_pts)} scene-change frames")
        return sorted(scene_pts)
    
    def extract_clip_stream(self, input_url: str, start: float, end: float, out_path: Path) -> Path:
        """
        Extract a clip by streaming just the needed portion using ffmpeg seek and duration flags.
        """
        dur = max(0.1, end - start)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        
        cmd = [
            "ffmpeg",
            "-hide_banner",
            "-ss", str(start),
            "-i", input_url,
            "-t", str(dur),
            "-c", "copy",
            str(out_path)
        ]
        self.logger.info(f"Extracting clip: {start:.2f}s - {end:.2f}s -> {out_path.name}")
        subprocess.run(cmd, check=True)
        return out_path
    
    def transcribe_whisper(self, model: Any, file_path: str) -> str:
        """Transcribe audio using Whisper."""
        if not WHISPER_AVAILABLE:
            self.logger.warning("Whisper not available, skipping transcription")
            return ""
        
        self.logger.info(f"Transcribing: {file_path}")
        res = model.transcribe(file_path)
        text = res.get('text', '').strip()
        return text
    
    def generate_metadata_from_transcript(self, transcript: str) -> Tuple[str, str, List[str]]:
        """Generate title, description and tags from transcript using TF-IDF."""
        if not transcript:
            return "", "", []
        
        if SKLEARN_AVAILABLE:
            return self._generate_metadata_tfidf(transcript)
        else:
            return self._generate_metadata_simple(transcript)
    
    def _generate_metadata_tfidf(self, transcript: str) -> Tuple[str, str, List[str]]:
        """Generate metadata using TF-IDF (requires scikit-learn)."""
        sentences = [s for s in re.split(r"(?<=[.!?])\\s+", transcript) if s]
        vectorizer = TfidfVectorizer(stop_words='english', max_features=200)
        
        try:
            X = vectorizer.fit_transform(sentences)
            feature_names = vectorizer.get_feature_names_out()
            sums = X.sum(axis=0).A1
            ranked = sorted(zip(feature_names, sums), key=lambda x: x[1], reverse=True)
            keywords = [w for w, _ in ranked][:10]
        except Exception:
            return self._generate_metadata_simple(transcript)
        
        # make a short title from top keywords
        title = " | ".join([k.capitalize() for k in keywords[:3]])
        if len(title) < 5:
            title = (transcript[:50] + "...") if len(transcript) > 50 else transcript
        
        # description: first 2 sentences + auto-hashtags
        desc = "\\n".join(sentences[:2])
        hashtags = [f"#{k.replace(' ', '')}" for k in keywords[:5]]
        description = desc + "\\n\\n" + "Discover more: " + " ".join(hashtags)
        tags = keywords[:15]
        
        return title[:100], description[:5000], tags
    
    def _generate_metadata_simple(self, transcript: str) -> Tuple[str, str, List[str]]:
        """Fallback metadata generation without TF-IDF."""
        words = re.findall(r"\\w+", transcript.lower())
        words = [w for w in words if len(w) > 3]
        keywords = [w for w, _ in Counter(words).most_common(10)]
        
        title = " | ".join([k.capitalize() for k in keywords[:3]])
        if len(title) < 5:
            title = (transcript[:50] + "...") if len(transcript) > 50 else transcript
        
        sentences = [s for s in re.split(r"(?<=[.!?])\\s+", transcript) if s]
        desc = "\\n".join(sentences[:2])
        hashtags = [f"#{k.replace(' ', '')}" for k in keywords[:5]]
        description = desc + "\\n\\n" + "Discover more: " + " ".join(hashtags)
        
        return title[:100], description[:5000], keywords
    
    def select_clip_ranges(self, scene_pts: List[float], video_duration: Optional[float] = None, 
                          max_clips: int = None) -> List[Tuple[float, float]]:
        """
        Build start/end ranges from scene timestamps.
        """
        if max_clips is None:
            max_clips = self.MAX_CLIPS_PER_RUN
        
        ranges = []
        if scene_pts:
            pts = [0.0] + scene_pts
            for i in range(len(pts)-1):
                s = pts[i]
                e = pts[i+1]
                if e - s < self.MIN_CLIP_SECONDS:
                    continue
                if e - s > self.MAX_CLIP_SECONDS:
                    e = s + self.MAX_CLIP_SECONDS
                ranges.append((s, e))
        
        # if still empty, fallback to greedy fixed segments
        if not ranges:
            if not video_duration:
                for i in range(max_clips):
                    s = i*60
                    e = s + 60
                    ranges.append((s, e))
            else:
                seg = min(60, self.MAX_CLIP_SECONDS)
                for i in range(int(video_duration/seg)):
                    s = i*seg
                    e = min(video_duration, s+seg)
                    ranges.append((s, e))
        
        return ranges[:max_clips]
    
    def process_video(self, url: str, dry_run: bool = False) -> Dict[str, Any]:
        """
        Main pipeline to process a video URL and create/upload clips.
        
        Args:
            url: Video URL to process
            dry_run: If True, don't upload to YouTube, just create clips
        
        Returns:
            Dict with processing results
        """
        self.CLIP_DIR.mkdir(parents=True, exist_ok=True)
        self.TMP_DIR.mkdir(parents=True, exist_ok=True)
        
        results = {
            "url": url,
            "clips_created": 0,
            "clips_uploaded": 0,
            "errors": [],
            "clips": []
        }
        
        try:
            # Step 1: Prepare input (download YouTube if needed) and detect scenes
            self.logger.info("1) Preparing input and detecting scene-change timestamps")
            try:
                source = self.prepare_input(url)
                scenes = self.run_ffmpeg_scene_detect(source)
            except subprocess.CalledProcessError as e:
                self.logger.warning(f"ffmpeg scene detection failed: {e}")
                scenes = []
            
            # Step 2: Select clip ranges
            self.logger.info("2) Selecting clip ranges")
            clip_ranges = self.select_clip_ranges(scenes, max_clips=self.MAX_CLIPS_PER_RUN)
            self.logger.info(f"Will extract {len(clip_ranges)} clips")
            
            # Step 3: Load Whisper model
            model = None
            if WHISPER_AVAILABLE and not dry_run:
                self.logger.info("3) Loading Whisper model")
                model = whisper.load_model(self.WHISPER_MODEL)
            
            # Step 4: YouTube auth (if not dry run)
            youtube = None
            if not dry_run and YOUTUBE_API_AVAILABLE:
                self.logger.info("4) Authorizing YouTube")
                try:
                    youtube = self.youtube_auth()
                except Exception as e:
                    results["errors"].append(f"YouTube auth failed: {str(e)}")
                    dry_run = True  # Fall back to dry run
            
            # Step 5: Process clips
            uploaded = 0
            for idx, (s, e) in enumerate(clip_ranges):
                clip_info = {"index": idx, "start": s, "end": e, "duration": e-s}
                out_file = self.CLIP_DIR / f"clip_{idx:03d}.mp4"
                
                try:
                    # Extract clip (use local source if we downloaded)
                    input_for_extract = source if 'source.' in (locals().get('source','')) else url
                    self.extract_clip_stream(input_for_extract, s, e, out_file)
                    clip_info["file_path"] = str(out_file)
                    clip_info["file_size"] = out_file.stat().st_size if out_file.exists() else 0
                    results["clips_created"] += 1
                    
                    # Transcribe if available
                    transcript = ""
                    if model:
                        transcript = self.transcribe_whisper(model, str(out_file))
                        clip_info["transcript"] = transcript
                    
                    # Generate metadata
                    title, description, tags = self.generate_metadata_from_transcript(transcript)
                    if not title:
                        title = f"Clip from {Path(url).name} #{idx}"
                    
                    clip_info.update({
                        "title": title,
                        "description": description,
                        "tags": tags
                    })
                    
                    self.logger.info(f"Generated title: {title}")
                    self.logger.info(f"Generated tags: {tags[:5]}")
                    
                    # Upload if not dry run
                    if not dry_run and youtube:
                        try:
                            youtube_resp = self.youtube_upload(youtube, str(out_file), title, description, tags)
                            clip_info["youtube_id"] = youtube_resp.get('id')
                            clip_info["uploaded"] = True
                            uploaded += 1
                            results["clips_uploaded"] += 1
                        except Exception as e:
                            error_msg = f"Upload failed for clip {idx}: {str(e)}"
                            self.logger.error(error_msg)
                            results["errors"].append(error_msg)
                            clip_info["uploaded"] = False
                    else:
                        clip_info["uploaded"] = False
                    
                    results["clips"].append(clip_info)
                    
                except Exception as e:
                    error_msg = f"Failed processing clip {idx}: {str(e)}"
                    self.logger.error(error_msg)
                    results["errors"].append(error_msg)
                    continue
                
                if uploaded >= self.MAX_CLIPS_PER_RUN:
                    self.logger.info("Reached upload limit for this run.")
                    break
            
            self.logger.info(f"Done. Created {results['clips_created']} clips, uploaded {results['clips_uploaded']}")
            
        except Exception as e:
            error_msg = f"Pipeline failed: {str(e)}"
            self.logger.error(error_msg)
            results["errors"].append(error_msg)
        
        return results


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: python auto_clip_uploader.py <video_url> [--dry-run]")
        sys.exit(1)
    
    url = sys.argv[1]
    dry_run = "--dry-run" in sys.argv
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    uploader = AutoClipUploader()
    results = uploader.process_video(url, dry_run=dry_run)
    
    print("\\n" + "="*50)
    print("PROCESSING RESULTS")
    print("="*50)
    print(f"URL: {results['url']}")
    print(f"Clips created: {results['clips_created']}")
    print(f"Clips uploaded: {results['clips_uploaded']}")
    print(f"Errors: {len(results['errors'])}")
    
    if results['errors']:
        print("\\nErrors:")
        for error in results['errors']:
            print(f"  - {error}")


if __name__ == '__main__':
    main()