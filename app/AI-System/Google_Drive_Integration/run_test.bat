@echo off
echo 🎭 Diva AI System - Google Drive Integration
echo ==========================================
echo.

echo 📍 Location: %~dp0
echo ⏰ Time: %date% %time%
echo.

echo 🔍 Checking Python...
python --version
if errorlevel 1 (
    echo ❌ Python not found! Please install Python 3.7+
    pause
    exit /b 1
)

echo.
echo ⚡ Running Quick Test...
echo.
python "%~dp0quick_test.py"

if errorlevel 1 (
    echo.
    echo ❌ Quick test failed!
    echo 🔧 Try running setup: python setup_drive.py
    echo.
    pause
    exit /b 1
)

echo.
echo ❓ Run full connection test? (y/n)
set /p choice="> "

if /i "%choice%"=="y" (
    echo.
    echo 🧪 Running Full Test...
    echo.
    python "%~dp0test_connection.py"
)

echo.
echo 🎉 Test completed!
echo.
pause