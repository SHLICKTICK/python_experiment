import os
import sys
import subprocess

def lock_screen():
    print(f"[*] Locking screen on {sys.platform}...")
    
    if sys.platform == "win32":
        # Windows
        import ctypes
        ctypes.windll.user32.LockWorkStation()
        
    elif sys.platform == "darwin":
        # macOS
        subprocess.run(["pmset", "displaysleepnow"])
        
    elif sys.platform.startswith("linux"):
        # Linux (Tries common desktop manager lock commands)
        try:
            # GNOME / Ubuntu default
            subprocess.run(["xdg-screensaver", "lock"])
        except FileNotFoundError:
            try:
                # KDE
                subprocess.run(["qdbus", "org.freedesktop.ScreenSaver", "/ScreenSaver", "Lock"])
            except FileNotFoundError:
                print("[-] Could not determine lock command for this Linux desktop environment.")
    else:
        print("[-] Unsupported operating system.")

if __name__ == "__main__":
    lock_screen()