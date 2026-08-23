import time
import os
import psutil

def format_speed(bytes_per_sec):
    """Converts bytes/sec to human-readable KB/s or MB/s."""
    if bytes_per_sec >= 1024 * 1024:
        return f"{bytes_per_sec / (1024 * 1024):6.2f} MB/s"
    else:
        return f"{bytes_per_sec / 1024:6.2f} KB/s"

def clear_console():
    """Clears terminal screen across Windows and Linux/macOS."""
    os.system('cls' if os.name == 'nt' else 'clear')

def monitor_bandwidth(interval=1):
    """Tracks and calculates network upload/download speeds."""
    print("[*] Initializing network throughput monitor...")
    
    # Get initial byte counts
    last_io = psutil.net_io_counters()
    last_time = time.time()

    try:
        while True:
            time.sleep(interval)
            
            # Get current byte counts and timestamp
            current_io = psutil.net_io_counters()
            current_time = time.time()
            
            # Calculate elapsed time and byte differences
            elapsed = current_time - last_time
            bytes_sent = current_io.bytes_sent - last_io.bytes_sent
            bytes_recv = current_io.bytes_recv - last_io.bytes_recv
            
            # Calculate transfer speeds per second
            upload_speed = bytes_sent / elapsed
            download_speed = bytes_recv / elapsed
            
            # Render live dashboard
            clear_console()
            print("==================================================")
            print("         LIVE NETWORK BANDWIDTH MONITOR           ")
            print("==================================================")
            print(f" Download Speed : {format_speed(download_speed)}")
            print(f" Upload Speed   : {format_speed(upload_speed)}")
            print("--------------------------------------------------")
            print(f" Total Downloaded: {current_io.bytes_recv / (1024 ** 2):.2f} MB")
            print(f" Total Uploaded  : {current_io.bytes_sent / (1024 ** 2):.2f} MB")
            print("==================================================")
            print("Press Ctrl+C to stop monitoring.")
            
            # Update previous metrics for the next iteration
            last_io = current_io
            last_time = current_time

    except KeyboardInterrupt:
        print("\n[*] Network monitoring stopped.")

if __name__ == "__main__":
    monitor_bandwidth(interval=1)