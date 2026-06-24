# JARVIS AI - Voice Recognition Module
# Listens for voice commands using sounddevice (no PyAudio needed)

import queue
import sys
import json

try:
    import sounddevice as sd
except ImportError:
    print("[ERROR] sounddevice not installed. Run: pip install sounddevice")
    sys.exit(1)

try:
    from vosk import Model, KaldiRecognizer
    USE_VOSK = True
except ImportError:
    USE_VOSK = False
    print("[INFO] Vosk not available, will use online speech recognition")
    import speech_recognition as sr

from config import WAKE_WORD


class Listener:
    """Handles all speech recognition functionality for JARVIS."""
    
    def __init__(self):
        """Initialize the speech recognizer."""
        self.sample_rate = 16000
        self.audio_queue = queue.Queue()
        self._use_online = True  # Default to online for now
        
        if USE_VOSK:
            # Offline recognition with Vosk
            print("[JARVIS] Loading offline speech model...")
            try:
                self.model = Model(lang="en-us")
                self.recognizer = KaldiRecognizer(self.model, self.sample_rate)
                self._use_online = False
                print("[JARVIS] Offline speech model loaded.")
            except Exception as e:
                print(f"[WARNING] Could not load Vosk model: {e}")
                print("[JARVIS] Using online recognition")
        
        if self._use_online:
            # Online recognition with SpeechRecognition
            self.sr_recognizer = sr.Recognizer()
        
        print("[JARVIS] Microphone ready.")
    
    def _audio_callback(self, indata, frames, time, status):
        """Callback for sounddevice stream."""
        if status:
            print(f"[DEBUG] Audio status: {status}", file=sys.stderr)
        self.audio_queue.put(bytes(indata))
    
    def listen_once(self) -> str:
        """
        Listen for speech and return recognized text.
        Returns the recognized text or empty string if failed.
        """
        if self._use_online:
            return self._listen_online()
        else:
            return self._listen_vosk()
    
    def _listen_vosk(self) -> str:
        """Listen using Vosk (offline)."""
        try:
            with sd.RawInputStream(
                samplerate=self.sample_rate,
                blocksize=8000,
                dtype='int16',
                channels=1,
                callback=self._audio_callback
            ):
                print("[JARVIS] Listening...")
                timeout_counter = 0
                max_timeout = 50  # About 5 seconds
                
                while timeout_counter < max_timeout:
                    try:
                        data = self.audio_queue.get(timeout=0.1)
                        if self.recognizer.AcceptWaveform(data):
                            result = json.loads(self.recognizer.Result())
                            text = result.get("text", "").strip()
                            if text:
                                print(f"[DEBUG] Heard: {text}")
                                return text.lower()
                    except queue.Empty:
                        timeout_counter += 1
                
                return ""
        except Exception as e:
            print(f"[ERROR] Microphone error: {e}")
            return ""
    
    def _listen_online(self) -> str:
        """Listen using Google Speech Recognition (online, uses sounddevice)."""
        try:
            import io
            import wave
            import numpy as np
            
            print("[JARVIS] Listening...")
            
            # Record audio using sounddevice
            duration = 5  # seconds
            recording = sd.rec(
                int(duration * self.sample_rate),
                samplerate=self.sample_rate,
                channels=1,
                dtype='int16'
            )
            sd.wait()  # Wait until recording is finished
            
            # Convert to WAV format for speech_recognition
            wav_buffer = io.BytesIO()
            with wave.open(wav_buffer, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)  # 16-bit
                wf.setframerate(self.sample_rate)
                wf.writeframes(recording.tobytes())
            
            wav_buffer.seek(0)
            
            # Use speech_recognition to process
            with sr.AudioFile(wav_buffer) as source:
                audio = self.sr_recognizer.record(source)
            
            text = self.sr_recognizer.recognize_google(audio)
            print(f"[DEBUG] Heard: {text}")
            return text.lower()
            
        except sr.UnknownValueError:
            return ""
        except sr.RequestError as e:
            print(f"[ERROR] Speech recognition error: {e}")
            return ""
        except Exception as e:
            print(f"[ERROR] Microphone error: {e}")
            return ""
    
    def listen_for_wake_word(self) -> bool:
        """Listen for the wake word."""
        text = self.listen_once()
        return WAKE_WORD in text
    
    def listen_for_command(self) -> str:
        """Listen for a command after wake word."""
        return self.listen_once()


# Test the listener if run directly
if __name__ == "__main__":
    listener = Listener()
    print("Say something...")
    text = listener.listen_once()
    print(f"You said: {text}")
