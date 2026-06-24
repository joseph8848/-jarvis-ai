# JARVIS AI - Text-to-Speech Module
# Gives JARVIS a voice

import pyttsx3
import random
from config import VOICE_RATE, VOICE_VOLUME, GREETINGS, ASSISTANT_NAME, USER_NAME


class Speaker:
    """Handles all text-to-speech functionality for JARVIS."""
    
    def __init__(self):
        """Initialize the speech engine."""
        self.engine = pyttsx3.init()
        self._setup_voice()
    
    def _setup_voice(self):
        """Configure voice properties."""
        # Set speech rate
        self.engine.setProperty('rate', VOICE_RATE)
        
        # Set volume
        self.engine.setProperty('volume', VOICE_VOLUME)
        
        # Try to find a British-sounding voice (like JARVIS)
        voices = self.engine.getProperty('voices')
        for voice in voices:
            # Look for a male English voice
            if 'david' in voice.name.lower() or 'male' in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                break
    
    def speak(self, text: str):
        """Speak the given text out loud."""
        print(f"[{ASSISTANT_NAME}]: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
    
    def greet(self):
        """Give a random greeting."""
        greeting = random.choice(GREETINGS)
        self.speak(greeting)
    
    def confirm_action(self, action: str):
        """Confirm an action to the user."""
        self.speak(f"{action}, {USER_NAME}.")
    
    def report_error(self, error: str):
        """Report an error to the user."""
        self.speak(f"I'm sorry {USER_NAME}, {error}")
    
    def say_goodbye(self):
        """Say goodbye before shutting down."""
        self.speak(f"Goodbye {USER_NAME}. Have a great day.")


# Test the speaker if run directly
if __name__ == "__main__":
    speaker = Speaker()
    speaker.speak("JARVIS online. All systems operational.")
