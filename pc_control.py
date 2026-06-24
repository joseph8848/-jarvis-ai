# JARVIS AI - PC Control Module
# Controls Windows applications and system functions

import os
import subprocess
import ctypes
from ctypes import cast, POINTER

# For volume control
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

from config import APPS


class PCController:
    """Controls Windows PC functions like launching apps, volume, etc."""
    
    def __init__(self):
        """Initialize the PC controller."""
        self._setup_volume_control()
    
    def _setup_volume_control(self):
        """Set up access to system volume."""
        try:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            self.volume = cast(interface, POINTER(IAudioEndpointVolume))
        except Exception as e:
            print(f"[WARNING] Could not initialize volume control: {e}")
            self.volume = None
    
    # ========== Application Control ==========
    
    def open_application(self, app_name: str) -> tuple[bool, str]:
        """
        Open an application by name.
        Returns (success, message).
        """
        app_name = app_name.lower().strip()
        
        # Check if app is in our predefined list
        if app_name in APPS:
            app_path = os.path.expandvars(APPS[app_name])
            try:
                subprocess.Popen(app_path)
                return True, f"Opening {app_name}"
            except FileNotFoundError:
                return False, f"Could not find {app_name} at the specified path"
            except Exception as e:
                return False, f"Error opening {app_name}: {str(e)}"
        
        # Try to open using Windows shell (for system apps)
        try:
            os.startfile(app_name)
            return True, f"Opening {app_name}"
        except Exception:
            pass
        
        # Try using subprocess with 'start' command
        try:
            subprocess.Popen(f'start {app_name}', shell=True)
            return True, f"Opening {app_name}"
        except Exception:
            pass
        
        return False, f"I couldn't find an application called {app_name}"
    
    def close_application(self, app_name: str) -> tuple[bool, str]:
        """
        Close an application by name.
        Returns (success, message).
        """
        app_name = app_name.lower().strip()
        
        try:
            # Use taskkill to close the application
            result = subprocess.run(
                f'taskkill /IM "{app_name}.exe" /F',
                shell=True,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return True, f"Closing {app_name}"
            else:
                return False, f"Could not close {app_name}"
        except Exception as e:
            return False, f"Error closing {app_name}: {str(e)}"
    
    # ========== Volume Control ==========
    
    def set_volume(self, level: int) -> tuple[bool, str]:
        """
        Set system volume to a percentage (0-100).
        Returns (success, message).
        """
        if self.volume is None:
            return False, "Volume control is not available"
        
        try:
            # Clamp level between 0 and 100
            level = max(0, min(100, level))
            # Convert to 0.0 - 1.0 range
            self.volume.SetMasterVolumeLevelScalar(level / 100, None)
            return True, f"Volume set to {level} percent"
        except Exception as e:
            return False, f"Could not set volume: {str(e)}"
    
    def get_volume(self) -> int:
        """Get current volume level (0-100)."""
        if self.volume is None:
            return -1
        try:
            return int(self.volume.GetMasterVolumeLevelScalar() * 100)
        except:
            return -1
    
    def mute(self) -> tuple[bool, str]:
        """Mute the system."""
        if self.volume is None:
            return False, "Volume control is not available"
        try:
            self.volume.SetMute(True, None)
            return True, "System muted"
        except Exception as e:
            return False, f"Could not mute: {str(e)}"
    
    def unmute(self) -> tuple[bool, str]:
        """Unmute the system."""
        if self.volume is None:
            return False, "Volume control is not available"
        try:
            self.volume.SetMute(False, None)
            return True, "System unmuted"
        except Exception as e:
            return False, f"Could not unmute: {str(e)}"
    
    def volume_up(self, amount: int = 10) -> tuple[bool, str]:
        """Increase volume by amount percent."""
        current = self.get_volume()
        if current < 0:
            return False, "Could not get current volume"
        return self.set_volume(current + amount)
    
    def volume_down(self, amount: int = 10) -> tuple[bool, str]:
        """Decrease volume by amount percent."""
        current = self.get_volume()
        if current < 0:
            return False, "Could not get current volume"
        return self.set_volume(current - amount)
    
    # ========== System Control ==========
    
    def lock_computer(self) -> tuple[bool, str]:
        """Lock the computer."""
        try:
            ctypes.windll.user32.LockWorkStation()
            return True, "Locking computer"
        except Exception as e:
            return False, f"Could not lock computer: {str(e)}"
    
    def shutdown(self, delay_seconds: int = 0) -> tuple[bool, str]:
        """Shutdown the computer with optional delay."""
        try:
            if delay_seconds > 0:
                subprocess.run(f'shutdown /s /t {delay_seconds}', shell=True)
                minutes = delay_seconds // 60
                return True, f"Computer will shutdown in {minutes} minutes"
            else:
                subprocess.run('shutdown /s /t 30', shell=True)
                return True, "Computer will shutdown in 30 seconds"
        except Exception as e:
            return False, f"Could not schedule shutdown: {str(e)}"
    
    def cancel_shutdown(self) -> tuple[bool, str]:
        """Cancel a scheduled shutdown."""
        try:
            subprocess.run('shutdown /a', shell=True)
            return True, "Shutdown cancelled"
        except Exception as e:
            return False, f"Could not cancel shutdown: {str(e)}"
    
    def restart(self) -> tuple[bool, str]:
        """Restart the computer."""
        try:
            subprocess.run('shutdown /r /t 30', shell=True)
            return True, "Computer will restart in 30 seconds"
        except Exception as e:
            return False, f"Could not restart: {str(e)}"
    
    def sleep(self) -> tuple[bool, str]:
        """Put the computer to sleep."""
        try:
            subprocess.run('rundll32.exe powrprof.dll,SetSuspendState 0,1,0', shell=True)
            return True, "Going to sleep"
        except Exception as e:
            return False, f"Could not sleep: {str(e)}"


# Test the controller if run directly
if __name__ == "__main__":
    pc = PCController()
    print(f"Current volume: {pc.get_volume()}%")
    success, msg = pc.set_volume(50)
    print(msg)
