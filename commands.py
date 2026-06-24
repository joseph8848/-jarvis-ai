# JARVIS AI - Command Processor
# Parses voice commands and determines actions

import re
from datetime import datetime
from pc_control import PCController


class CommandProcessor:
    """Processes voice commands and executes appropriate actions."""
    
    def __init__(self, pc_controller: PCController):
        """Initialize with a PC controller instance."""
        self.pc = pc_controller
    
    def process(self, command: str) -> tuple[bool, str]:
        """
        Process a voice command.
        Returns (success, response_message).
        """
        command = command.lower().strip()
        
        # Remove wake word if present
        command = command.replace("jarvis", "").strip()
        
        # Try each command pattern
        handlers = [
            self._handle_open_app,
            self._handle_close_app,
            self._handle_volume,
            self._handle_mute,
            self._handle_system,
            self._handle_time,
            self._handle_date,
            self._handle_greeting,
            self._handle_goodbye,
        ]
        
        for handler in handlers:
            result = handler(command)
            if result is not None:
                return result
        
        # No matching command found
        return False, "I'm not sure how to help with that. Could you try again?"
    
    # ========== Command Handlers ==========
    
    def _handle_open_app(self, command: str) -> tuple[bool, str] | None:
        """Handle 'open [app]' commands."""
        patterns = [
            r"open\s+(.+)",
            r"launch\s+(.+)",
            r"start\s+(.+)",
            r"run\s+(.+)",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, command)
            if match:
                app_name = match.group(1).strip()
                return self.pc.open_application(app_name)
        
        return None
    
    def _handle_close_app(self, command: str) -> tuple[bool, str] | None:
        """Handle 'close [app]' commands."""
        patterns = [
            r"close\s+(.+)",
            r"quit\s+(.+)",
            r"exit\s+(.+)",
            r"kill\s+(.+)",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, command)
            if match:
                app_name = match.group(1).strip()
                return self.pc.close_application(app_name)
        
        return None
    
    def _handle_volume(self, command: str) -> tuple[bool, str] | None:
        """Handle volume commands."""
        # Set volume to specific level
        match = re.search(r"(?:set\s+)?volume\s+(?:to\s+)?(\d+)(?:\s*percent)?", command)
        if match:
            level = int(match.group(1))
            return self.pc.set_volume(level)
        
        # Volume up
        if any(phrase in command for phrase in ["volume up", "louder", "turn up", "increase volume"]):
            # Check if specific amount mentioned
            match = re.search(r"(\d+)", command)
            amount = int(match.group(1)) if match else 10
            return self.pc.volume_up(amount)
        
        # Volume down
        if any(phrase in command for phrase in ["volume down", "quieter", "turn down", "decrease volume", "lower volume"]):
            match = re.search(r"(\d+)", command)
            amount = int(match.group(1)) if match else 10
            return self.pc.volume_down(amount)
        
        # Get current volume
        if "what" in command and "volume" in command:
            level = self.pc.get_volume()
            if level >= 0:
                return True, f"The volume is at {level} percent"
            return False, "I couldn't check the volume"
        
        return None
    
    def _handle_mute(self, command: str) -> tuple[bool, str] | None:
        """Handle mute/unmute commands."""
        if "unmute" in command:
            return self.pc.unmute()
        if "mute" in command:
            return self.pc.mute()
        return None
    
    def _handle_system(self, command: str) -> tuple[bool, str] | None:
        """Handle system commands (lock, shutdown, restart, sleep)."""
        # Lock computer
        if "lock" in command and ("computer" in command or "pc" in command or "screen" in command):
            return self.pc.lock_computer()
        
        # Cancel shutdown
        if "cancel" in command and "shutdown" in command:
            return self.pc.cancel_shutdown()
        
        # Shutdown
        if "shutdown" in command or "shut down" in command:
            # Check for delay
            match = re.search(r"(\d+)\s*(?:minute|min)", command)
            if match:
                minutes = int(match.group(1))
                return self.pc.shutdown(minutes * 60)
            return self.pc.shutdown()
        
        # Restart
        if "restart" in command or "reboot" in command:
            return self.pc.restart()
        
        # Sleep
        if "sleep" in command:
            return self.pc.sleep()
        
        return None
    
    def _handle_time(self, command: str) -> tuple[bool, str] | None:
        """Handle time queries."""
        if "time" in command and ("what" in command or "tell" in command):
            now = datetime.now()
            time_str = now.strftime("%I:%M %p")
            return True, f"The time is {time_str}"
        return None
    
    def _handle_date(self, command: str) -> tuple[bool, str] | None:
        """Handle date queries."""
        if "date" in command and ("what" in command or "tell" in command):
            now = datetime.now()
            date_str = now.strftime("%A, %B %d, %Y")
            return True, f"Today is {date_str}"
        
        if "day" in command and ("what" in command or "which" in command):
            now = datetime.now()
            day_str = now.strftime("%A")
            return True, f"Today is {day_str}"
        
        return None
    
    def _handle_greeting(self, command: str) -> tuple[bool, str] | None:
        """Handle greetings."""
        greetings = ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"]
        if any(g in command for g in greetings):
            return True, "Hello! How can I help you today?"
        return None
    
    def _handle_goodbye(self, command: str) -> tuple[bool, str] | None:
        """Handle goodbye commands (these trigger shutdown of JARVIS)."""
        if any(phrase in command for phrase in ["goodbye", "bye", "go to sleep", "that's all", "i'm done"]):
            return True, "GOODBYE"  # Special signal to main loop
        return None
