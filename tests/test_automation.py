"""
Basic tests for the automation framework.
"""

import sys
import pytest
from pathlib import Path

# Add the src directory to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.config_manager import ConfigManager
from src.automation_framework import AutomationFramework


def test_config_manager_initialization():
    """Test that ConfigManager initializes properly."""
    config_manager = ConfigManager()
    assert config_manager.is_loaded()
    
    config = config_manager.get_config()
    assert "app_name" in config
    assert config["app_name"] == "Automation Framework"


def test_automation_framework_initialization():
    """Test that AutomationFramework initializes properly."""
    config_manager = ConfigManager()
    framework = AutomationFramework(config_manager)
    
    tasks = framework.list_tasks()
    assert "hello_world" in tasks
    assert "system_check" in tasks
    assert "cleanup" in tasks
    assert "clip_uploader" in tasks


def test_hello_world_task():
    """Test the hello world task."""
    config_manager = ConfigManager()
    framework = AutomationFramework(config_manager)
    
    result = framework.run_task("hello_world")
    assert result is True


def test_system_check_task():
    """Test the system check task."""
    config_manager = ConfigManager()
    framework = AutomationFramework(config_manager)
    
    result = framework.run_task("system_check")
    assert result is True


def test_invalid_task():
    """Test running an invalid task."""
    config_manager = ConfigManager()
    framework = AutomationFramework(config_manager)
    
    result = framework.run_task("nonexistent_task")
    assert result is False


def test_task_status():
    """Test getting task status."""
    config_manager = ConfigManager()
    framework = AutomationFramework(config_manager)
    
    status = framework.get_task_status()
    assert "tasks_available" in status
    assert "task_list" in status
    assert "framework_ready" in status
    assert status["framework_ready"] is True


if __name__ == "__main__":
    pytest.main([__file__])