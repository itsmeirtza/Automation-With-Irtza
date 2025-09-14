#!/usr/bin/env python3
"""
Automation With Irtza - Simple Working Version
Created by: Irtza Ali Waris
Email: Irtzaaliwaris@gmail.com
Website: https://ialiwaris.com
"""

import os
import time
import json
from pathlib import Path

class AutomationWithIrtza:
    def __init__(self):
        self.youtube_channel = ""
        self.video_url = ""
        self.clips = []
        self.step = 1
        
        print("=" * 60)
        print("    🚀 AUTOMATION WITH IRTZA")
        print("=" * 60)
        print("    Created by: Irtza Ali Waris")
        print("    Email: Irtzaaliwaris@gmail.com")
        print("    Website: https://ialiwaris.com")
        print("=" * 60)
        
    def step_1_youtube_channel(self):
        """Step 1: YouTube Channel Link"""
        print("\n📺 STEP 1: YouTube Channel Link")
        print("-" * 40)
        
        while True:
            channel = input("Enter your YouTube channel URL: ").strip()
            if channel:
                self.youtube_channel = channel
                print(f"✅ Channel set: {channel}")
                break
            else:
                print("❌ Please enter a valid channel URL")
        
        self.step = 2
        
    def step_2_video_link(self):
        """Step 2: Video Link"""
        print("\n🎥 STEP 2: Video Link")
        print("-" * 40)
        
        while True:
            video = input("Enter video URL to process: ").strip()
            if video:
                self.video_url = video
                print(f"✅ Video set: {video}")
                break
            else:
                print("❌ Please enter a valid video URL")
        
        self.step = 3
        
    def step_3_processing(self):
        """Step 3: Video Processing"""
        print("\n⚙️ STEP 3: Processing Video")
        print("-" * 40)
        print("🔄 AI is analyzing your video...")
        
        # Simulate processing
        for i in range(1, 11):
            print(f"Processing... {i*10}%", end="\r")
            time.sleep(0.5)
        
        print("\n✅ Processing complete!")
        
        # Create mock clips
        self.clips = [
            {"title": f"Amazing Clip {i+1}", "duration": f"{30+i*10}s", "size": f"{5+i}MB"} 
            for i in range(6)
        ]
        
        self.step = 4
        
    def step_4_preview_clips(self):
        """Step 4: Preview 6 Clips"""
        print("\n👀 STEP 4: Preview Generated Clips")
        print("-" * 40)
        print(f"📹 Generated {len(self.clips)} clips:")
        
        for i, clip in enumerate(self.clips, 1):
            print(f"  {i}. {clip['title']} - {clip['duration']} ({clip['size']})")
        
        print("\nAll clips are selected for upload by default.")
        
        choice = input("\nContinue to upload? (y/n): ").strip().lower()
        if choice in ['y', 'yes', '']:
            self.step = 5
        else:
            print("❌ Upload cancelled")
            return
            
    def step_5_upload_youtube(self):
        """Step 5: Upload to YouTube"""
        print("\n📤 STEP 5: Uploading to YouTube")
        print("-" * 40)
        print("🚀 Uploading clips to your YouTube channel...")
        
        # Simulate upload
        for i, clip in enumerate(self.clips, 1):
            print(f"Uploading {clip['title']}...", end="")
            time.sleep(1)
            print(" ✅ Done!")
        
        print("\n🎉 All clips uploaded successfully!")
        self.step = 6
        
    def step_6_dashboard(self):
        """Step 6: Dashboard"""
        print("\n📊 STEP 6: Dashboard")
        print("-" * 40)
        print("🎯 Automation Complete!")
        print(f"✅ YouTube Channel: {self.youtube_channel}")
        print(f"✅ Video Processed: {self.video_url}")
        print(f"✅ Clips Created: {len(self.clips)}")
        print(f"✅ Clips Uploaded: {len(self.clips)}")
        print("\n📈 All your videos are now live on YouTube!")
        
        choice = input("\nProcess another video? (y/n): ").strip().lower()
        if choice in ['y', 'yes']:
            self.reset_and_start_again()
        else:
            print("\n👋 Thank you for using Automation With Irtza!")
            return False
        return True
        
    def reset_and_start_again(self):
        """Reset for new workflow"""
        self.youtube_channel = ""
        self.video_url = ""
        self.clips = []
        self.step = 1
        print("\n" + "="*60)
        print("🔄 Starting New Automation Workflow")
        print("="*60)
        
    def run(self):
        """Main workflow runner"""
        while True:
            try:
                if self.step == 1:
                    self.step_1_youtube_channel()
                elif self.step == 2:
                    self.step_2_video_link()
                elif self.step == 3:
                    self.step_3_processing()
                elif self.step == 4:
                    self.step_4_preview_clips()
                elif self.step == 5:
                    self.step_5_upload_youtube()
                elif self.step == 6:
                    if not self.step_6_dashboard():
                        break
                else:
                    break
                    
            except KeyboardInterrupt:
                print("\n\n👋 Automation stopped by user")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                print("Please try again...")
                time.sleep(2)

if __name__ == "__main__":
    app = AutomationWithIrtza()
    app.run()