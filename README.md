# JARVIS AI Assistant

[🚀 Run Locally](#quick-start) - *Run with `python main.py`*

A local, voice-controlled AI assistant for Windows PC.

## Quick Start

### 1. Install Python
Download and install Python 3.10 or higher from:
https://www.python.org/downloads/

**Important:** During installation, check ✅ "Add Python to PATH"

### 2. Install Dependencies
Open Command Prompt in this folder and run:
```
pip install -r requirements.txt
```

**Note:** If PyAudio fails to install, download the wheel from:
https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio

### 3. Run JARVIS
```
python main.py
```

## Usage

Say "JARVIS" followed by a command:

| Command | Example |
|---------|---------|
| Open apps | "JARVIS, open Chrome" |
| Close apps | "JARVIS, close Notepad" |
| Volume | "JARVIS, volume 50" |
| Volume up/down | "JARVIS, volume up" |
| Mute/Unmute | "JARVIS, mute" |
| Time | "JARVIS, what time is it?" |
| Date | "JARVIS, what's the date?" |
| Lock PC | "JARVIS, lock the computer" |
| Shutdown | "JARVIS, shutdown in 10 minutes" |
| Exit | "JARVIS, goodbye" |

## Files

- `main.py` - Entry point, start JARVIS here
- `config.py` - Settings and app paths (customize here!)
- `listener.py` - Voice recognition
- `speaker.py` - Text-to-speech
- `commands.py` - Command processing
- `pc_control.py` - Windows automation

## Customization

Edit `config.py` to:
- Change wake word (default: "jarvis")
- Add your app paths
- Change voice settings
- Personalize responses

## Troubleshooting

**Microphone not working:**
- Check Windows microphone permissions
- Make sure a microphone is set as default

**PyAudio installation fails:**
- Install Visual C++ Build Tools, or
- Download pre-built wheel from unofficial binaries

**App won't open:**
- Add the correct path to APPS in config.py
