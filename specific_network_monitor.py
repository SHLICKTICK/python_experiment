import os
import sys
import time
from collections import defaultdict
import psutil

def is_admin():
    """Checks if the script is running with elevated privileges."""
    try:
        return os.getuid() == 0  # Linux/macOS
    except AttributeError:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0  # Windows

def format_bytes(b):
    """Formats bytes into human-readable strings."""
    if b >= 1024 * 1024:
        return f"{b / (1024 * 1024):6.2f} MB/s"
    elif b >= 1024:
        return f"{b / 1024:6.2f} KB/s"
    return f"{b:6.2f} B/s"

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_process_connections():
    """Maps active network connections to active PIDs."""
    pid_map = set()
    try:
        # Get active TCP/UDP connections across all interfaces
        for conn in psutil.net_connections(kind='inet'):
            if conn.pid and conn.status == psutil.CONN_ESTABLISHED:
                pid_map.add(conn.pid)
    except (psutil.AccessDenied, PermissionError):
        pass
    return pid_map

def monitor_processes(interval=1):
    if not is_admin():
        print("[!] WARNING: Per-process network inspection requires Administrator privileges.")
        print("[!] Please restart your terminal/VS Code as Administrator to see process details.\n")
        time.sleep(2)

    print("[*] Tracking per-process network activity...")

    # Stores byte counters per process ID: {pid: (bytes_sent, bytes_recv)}
    proc_io_history = {}

    try:
        while True:
            active_pids = get_process_connections()
            current_rates = []

            for pid in active_pids:
                try:
                    proc = psutil.Process(pid)
                    # Note: psutil proc.io_counters() tracks disk+net IO combined on some OS platforms,
                    # but provides a clear baseline for tracking highest active network processes.
                    io = proc.io_counters()
                    
                    if pid in proc_io_history:
                        old_read, old_write = proc_io_history[pid]
                        read_rate = (io.read_bytes - old_read) / interval
                        write_rate = (io.write_bytes - old_write) / interval
                        total_rate = read_rate + write_rate
                        
                        if total_rate > 0:
                            current_rates.append((proc.name(), pid, read_rate, write_rate, total_rate))

                    proc_io_history[pid] = (io.read_bytes, io.write_bytes)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            # Sort processes by total throughput (highest first)
            current_rates.sort(key=lambda x: x[4], reverse=True)

            # Overall System Bandwidth
            sys_io = psutil.net_io_counters()

            clear_console()
            print("==========================================================================")
            print("                 TOP NETWORK-CONSUMING PROCESSES                          ")
            print("==========================================================================")
            print(f"{'PROCESS NAME':<25} {'PID':<8} {'DOWNLOAD (READ)':<18} {'UPLOAD (WRITE)':<18}")
            print("--------------------------------------------------------------------------")

            if not current_rates:
                print("  No active process bandwidth spikes detected in this interval...")
            else:
                for name, pid, r_rate, w_rate, _ in current_rates[:10]:  # Top 10 processes
                    print(f"{name:<25} {pid:<8} {format_bytes(r_rate):<18} {format_bytes(w_rate):<18}")

            print("==========================================================================")
            print("Press Ctrl+C to exit.")

            time.sleep(interval)

    except KeyboardInterrupt:
        print("\n[*] Monitor stopped.")

if __name__ == "__main__":
    monitor_processes(interval=1)