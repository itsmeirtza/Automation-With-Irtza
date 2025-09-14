#!/usr/bin/env python3
"""
Main entry point for the automation project.

This module provides the primary interface for running automation tasks.
"""

import argparse
import logging
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.automation_framework import AutomationFramework
from src.config_manager import ConfigManager


def setup_logging(log_level: str = "INFO") -> None:
    """Configure logging for the application."""
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format=log_format,
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("logs/automation.log")
        ]
    )


def main() -> int:
    """Main entry point for the automation application."""
    parser = argparse.ArgumentParser(description="Automation Framework")
    parser.add_argument(
        "--config", 
        type=str, 
        default="config/default.json",
        help="Path to configuration file"
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging level"
    )
    parser.add_argument(
        "--task",
        type=str,
        help="Specific task to run"
    )
    parser.add_argument(
        "--list-tasks",
        action="store_true",
        help="List available tasks"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.log_level)
    logger = logging.getLogger(__name__)
    
    try:
        # Initialize configuration manager
        config_manager = ConfigManager(args.config)
        
        # Initialize automation framework
        framework = AutomationFramework(config_manager)
        
        if args.list_tasks:
            tasks = framework.list_tasks()
            print("Available tasks:")
            for task in tasks:
                print(f"  - {task}")
            return 0
        
        if args.task:
            logger.info(f"Running task: {args.task}")
            result = framework.run_task(args.task)
            if result:
                logger.info("Task completed successfully")
                return 0
            else:
                logger.error("Task failed")
                return 1
        else:
            # Run default automation workflow
            logger.info("Starting automation framework")
            framework.run_default_workflow()
            logger.info("Automation completed")
            return 0
            
    except Exception as e:
        logger.error(f"Automation failed: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())