@echo off
title Automation With Irtza - Video Automation Framework
color 0A

echo.
echo ================================================================
echo     🚀 AUTOMATION WITH IRTZA - VIDEO AUTOMATION FRAMEWORK
echo ================================================================
echo     Created by: Irtza Ali Waris
echo     Email: Irtzaaliwaris@gmail.com
echo     Website: https://ialiwaris.com
echo ================================================================
echo.

echo 🔍 Starting application...
echo.

REM Try different Python commands
python run.py
if %errorlevel% neq 0 (
    echo Python not found, trying py...
    py run.py
    if %errorlevel% neq 0 (
        echo.
        echo ❌ Python not found! Please install Python 3.8+ from:
        echo    https://python.org
        echo.
        pause
        exit /b 1
    )
)

pause