# JARVIS AI - Main Entry Point
# "JARVIS online. All systems operational."

import time
import sys

from config import WAKE_WORD, ASSISTANT_NAME
from listener import Listener
from speaker import Speaker
from pc_control import PCController
from commands import CommandProcessor


class JARVIS:
    """Main JARVIS AI assistant class."""
    
    def __init__(self):
        """Initialize all JARVIS components."""
        print(f"\n{'='*50}")
        print(f"  {ASSISTANT_NAME} - AI Assistant")
        print(f"  Initializing systems...")
        print(f"{'='*50}\n")
        
        # Initialize components
        self.speaker = Speaker()
        self.listener = Listener()
        self.pc_controller = PCController()
        self.command_processor = CommandProcessor(self.pc_controller)
        
        self.running = False
    
    def startup(self):
        """Perform startup sequence."""
        self.speaker.speak(f"{ASSISTANT_NAME} online. All systems operational.")
        self.speaker.speak(f"Say '{WAKE_WORD}' followed by a command to get started.")
        self.running = True
    
    def shutdown(self):
        """Perform shutdown sequence."""
        self.running = False
        self.speaker.say_goodbye()
        print(f"\n[{ASSISTANT_NAME}] Shutting down...\n")
    
    def run(self):
        """Main loop - listen for commands and process them."""
        self.startup()
        
        print(f"\n[INFO] Listening for '{WAKE_WORD}'...")
        print("[INFO] Press Ctrl+C to exit\n")
        
        try:
            while self.running:
                # Listen for any speech
                text = self.listener.listen_once()
                
                if not text:
                    continue
                
                # Check if wake word was said
                if WAKE_WORD not in text:
                    continue
                
                # Wake word detected!
                print(f"\n[{ASSISTANT_NAME}] Wake word detected!")
                
                # Extract command (everything after wake word)
                command = text
                
                # If command was included with wake word
                if len(text.replace(WAKE_WORD, "").strip()) > 0:
                    command = text
                else:
                    # Wake word only - listen for the command
                    self.speaker.speak("Yes?")
                    command = self.listener.listen_for_command()
                    
                    if not command:
                        self.speaker.speak("I didn't catch that. Please try again.")
                        continue
                
                # Process the command
                print(f"[{ASSISTANT_NAME}] Processing: '{command}'")
                success, response = self.command_processor.process(command)
                
                # Check for shutdown signal
                if response == "GOODBYE":
                    self.shutdown()
                    break
                
                # Speak the response
                if success:
                    self.speaker.confirm_action(response)
                else:
                    self.speaker.report_error(response)
                
                # Brief pause before listening again
                time.sleep(0.5)
                
        except KeyboardInterrupt:
            print("\n\n[INFO] Keyboard interrupt received")
            self.shutdown()
        except Exception as e:
            print(f"\n[ERROR] Unexpected error: {e}")
            self.speaker.speak("I've encountered an error and need to restart.")
            self.shutdown()


def main():
    """Entry point for JARVIS."""
    print("\nStarting JARVIS AI Assistant...")
    print("=" * 50)
    
    try:
        jarvis = JARVIS()
        jarvis.run()
    except Exception as e:
        print(f"\n[FATAL ERROR] Failed to start JARVIS: {e}")
        print("\nMake sure all dependencies are installed:")
        print("  pip install SpeechRecognition pyttsx3 pyautogui pywinauto pycaw comtypes")
        sys.exit(1)


if __name__ == "__main__":
    main()
