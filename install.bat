@echo off
echo ================================================
echo   JARVIS AI - Installation Helper
echo ================================================
echo.
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [ERROR] Python is not installed!
    echo.
    echo Please install Python 3.10 or higher from:
    echo https://www.python.org/downloads/
    echo.
    echo IMPORTANT: Check "Add Python to PATH" during installation!
    echo.
    start https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Python found!
python --version
echo.

echo Installing dependencies...
echo.
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo [WARNING] Some packages may have failed to install.
    echo If PyAudio failed, you can try:
    echo   pip install pipwin
    echo   pipwin install pyaudio
    echo.
)

echo.
echo ================================================
echo   Installation Complete!
echo ================================================
echo.
echo To start JARVIS, run:
echo   python main.py
echo.
echo Or double-click: start_jarvis.bat
echo.
pause
