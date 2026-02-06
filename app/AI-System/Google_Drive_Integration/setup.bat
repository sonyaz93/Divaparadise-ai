@echo off
echo 🎭 Diva AI System - Google Drive Integration Setup
echo ==================================================
echo.

echo 📍 Location: %~dp0
echo ⏰ Time: %date% %time%
echo.

echo 🔍 Checking Python...
python --version
if errorlevel 1 (
    echo ❌ Python not found! Please install Python 3.7+
    echo 📥 Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo.
echo 🚀 Running Setup...
echo.
python "%~dp0setup_drive.py"

if errorlevel 1 (
    echo.
    echo ❌ Setup failed!
    echo 📝 Please check the error messages above
) else (
    echo.
    echo 🎉 Setup completed successfully!
)

echo.
pause