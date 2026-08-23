import subprocess
import time
import pyautogui

# Open Notepad
subprocess.Popen(["notepad.exe"])

# Wait 1 second for Notepad to open
time.sleep(1)

# Type "hello" into Notepad
pyautogui.write("hello", interval=0.1)