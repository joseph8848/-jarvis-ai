# JARVIS AI - Configuration
# All settings and paths

# Wake word - say this to activate JARVIS
WAKE_WORD = "jarvis"

# Voice settings
VOICE_RATE = 180  # Speed of speech (words per minute)
VOICE_VOLUME = 1.0  # Volume 0.0 to 1.0

# Application paths (customize these for your PC)
APPS = {
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "firefox": r"C:\Program Files\Mozilla Firefox\firefox.exe",
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "explorer": "explorer.exe",
    "word": r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
    "excel": r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
    "archicad": r"C:\Program Files\GRAPHISOFT\ArchiCAD 27\ArchiCAD.exe",
    "spotify": r"C:\Users\%USERNAME%\AppData\Roaming\Spotify\Spotify.exe",
    "vscode": r"C:\Users\%USERNAME%\AppData\Local\Programs\Microsoft VS Code\Code.exe",
}

# Personalisation
ASSISTANT_NAME = "JARVIS"
USER_NAME = "Sir"  # How JARVIS addresses you

# Response phrases
GREETINGS = [
    f"Hello {USER_NAME}, how can I help you?",
    f"At your service, {USER_NAME}.",
    f"Yes {USER_NAME}?",
    f"Ready for your command, {USER_NAME}.",
]
