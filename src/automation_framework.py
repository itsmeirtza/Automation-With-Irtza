"""
Core automation framework module.

This module provides the main automation framework class that orchestrates
various automation tasks and workflows.
"""

import logging
import time
from typing import Dict, List, Any, Optional
from datetime import datetime

from src.config_manager import ConfigManager
from src.auto_clip_uploader import AutoClipUploader


class AutomationFramework:
    """Main automation framework class."""
    
    def __init__(self, config_manager: ConfigManager):
        """Initialize the automation framework."""
        self.config_manager = config_manager
        self.logger = logging.getLogger(__name__)
        self.tasks = {}
        self._initialize_tasks()
    
    def _initialize_tasks(self) -> None:
        """Initialize available automation tasks."""
        # Register built-in tasks
        self.tasks = {
            "hello_world": self._hello_world_task,
            "system_check": self._system_check_task,
            "cleanup": self._cleanup_task,
            "clip_uploader": self._clip_uploader_task,
        }
        
        # Initialize clip uploader
        self.clip_uploader = AutoClipUploader()
        
        self.logger.info(f"Initialized {len(self.tasks)} automation tasks")
    
    def list_tasks(self) -> List[str]:
        """Return a list of available tasks."""
        return list(self.tasks.keys())
    
    def run_task(self, task_name: str) -> bool:
        """Run a specific automation task."""
        if task_name not in self.tasks:
            self.logger.error(f"Task '{task_name}' not found")
            return False
        
        try:
            self.logger.info(f"Starting task: {task_name}")
            start_time = time.time()
            
            result = self.tasks[task_name]()
            
            end_time = time.time()
            execution_time = end_time - start_time
            
            self.logger.info(f"Task '{task_name}' completed in {execution_time:.2f} seconds")
            return result
            
        except Exception as e:
            self.logger.error(f"Task '{task_name}' failed: {str(e)}")
            return False
    
    def run_default_workflow(self) -> None:
        """Run the default automation workflow."""
        self.logger.info("Starting default automation workflow")
        
        # Get workflow configuration
        config = self.config_manager.get_config()
        workflow_tasks = config.get("default_workflow", ["hello_world", "system_check"])
        
        for task_name in workflow_tasks:
            success = self.run_task(task_name)
            if not success:
                self.logger.warning(f"Task '{task_name}' failed, continuing with next task")
        
        self.logger.info("Default workflow completed")
    
    def _hello_world_task(self) -> bool:
        """A simple hello world task."""
        self.logger.info("Hello World from Automation Framework!")
        print("Hello World! Automation is running successfully.")
        return True
    
    def _system_check_task(self) -> bool:
        """Perform basic system checks."""
        self.logger.info("Performing system checks...")
        
        # Check current time
        current_time = datetime.now()
        self.logger.info(f"Current time: {current_time}")
        
        # Check configuration
        config = self.config_manager.get_config()
        self.logger.info(f"Configuration loaded: {len(config)} settings")
        
        # Mock system resource check
        self.logger.info("System resources: OK")
        self.logger.info("Network connectivity: OK")
        self.logger.info("Storage space: OK")
        
        print("System check completed successfully!")
        return True
    
    def _cleanup_task(self) -> bool:
        """Perform cleanup operations."""
        self.logger.info("Performing cleanup operations...")
        
        # Mock cleanup operations
        self.logger.info("Cleaning temporary files...")
        time.sleep(1)  # Simulate work
        
        self.logger.info("Optimizing logs...")
        time.sleep(1)  # Simulate work
        
        self.logger.info("Cleanup completed successfully")
        print("Cleanup task completed!")
        return True
    
    def add_custom_task(self, name: str, task_function) -> None:
        """Add a custom task to the framework."""
        self.tasks[name] = task_function
        self.logger.info(f"Added custom task: {name}")
    
    def _clip_uploader_task(self) -> bool:
        """Auto clip uploader task."""
        self.logger.info("Running Auto Clip Uploader task...")
        
        # Get configuration for clip uploader
        config = self.config_manager.get_config()
        task_config = config.get("task_settings", {}).get("clip_uploader", {})
        
        if not task_config.get("enabled", False):
            self.logger.info("Clip uploader task is disabled")
            return True
        
        video_url = task_config.get("video_url")
        if not video_url:
            self.logger.error("No video URL configured for clip uploader task")
            self.logger.info("Set 'task_settings.clip_uploader.video_url' in configuration")
            return False
        
        dry_run = task_config.get("dry_run", True)  # Default to dry run for safety
        
        try:
            results = self.clip_uploader.process_video(video_url, dry_run=dry_run)
            
            self.logger.info(f"Clip processing results:")
            self.logger.info(f"  - URL: {results['url']}")
            self.logger.info(f"  - Clips created: {results['clips_created']}")
            self.logger.info(f"  - Clips uploaded: {results['clips_uploaded']}")
            self.logger.info(f"  - Errors: {len(results['errors'])}")
            
            if results['errors']:
                self.logger.warning("Errors occurred during clip processing:")
                for error in results['errors']:
                    self.logger.warning(f"  - {error}")
            
            print(f"Auto Clip Uploader completed: {results['clips_created']} clips created, {results['clips_uploaded']} uploaded")
            return len(results['errors']) == 0
            
        except Exception as e:
            self.logger.error(f"Clip uploader task failed: {str(e)}")
            return False
    
    def get_task_status(self) -> Dict[str, Any]:
        """Get the status of the automation framework."""
        return {
            "tasks_available": len(self.tasks),
            "task_list": list(self.tasks.keys()),
            "config_loaded": self.config_manager.is_loaded(),
            "framework_ready": True
        }
