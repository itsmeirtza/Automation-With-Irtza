@echo off
title Automation With Irtza - Simple Version
color 0A

echo.
echo ================================================================
echo     🚀 AUTOMATION WITH IRTZA - SIMPLE WORKING VERSION
echo ================================================================
echo     Created by: Irtza Ali Waris
echo     Email: Irtzaaliwaris@gmail.com  
echo     Website: https://ialiwaris.com
echo ================================================================
echo.

echo 🚀 Starting simple automation workflow...
echo.

python simple_app.py
if %errorlevel% neq 0 (
    echo.
    echo Trying with 'py' command...
    py simple_app.py
)

echo.
echo Press any key to exit...
pause >nul