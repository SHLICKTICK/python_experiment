import os
import platform
import socket
from datetime import datetime
import psutil
import requests

def get_public_ip():
    """Fetches the external public IP address using an online API."""
    try:
        response = requests.get('https://api.ipify.org?format=json', timeout=5)
        return response.json().get('ip', 'Unavailable')
    except Exception:
        return 'Unavailable (Offline or Request Failed)'

def get_network_interfaces():
    """Maps network interface names to their MAC and IP addresses."""
    interfaces = {}
    net_addrs = psutil.net_if_addrs()
    
    for interface_name, addrs in net_addrs.items():
        ip_addr = "N/A"
        mac_addr = "N/A"
        for addr in addrs:
            # Address family socket AF_INET corresponds to IPv4
            if addr.family == socket.AF_INET:
                ip_addr = addr.address
            # MAC address family varies by OS (AF_LINK or psutil constant)
            elif addr.family == getattr(psutil, 'AF_LINK', None) or addr.family == getattr(socket, 'AF_LINK', -1):
                mac_addr = addr.address

        # Only list interfaces that have either an active IP or MAC
        if ip_addr != "N/A" or mac_addr != "N/A":
            interfaces[interface_name] = f"IP: {ip_addr} | MAC: {mac_addr}"
            
    return interfaces

def get_disk_usage():
    """Gathers storage usage across all mounted disk partitions."""
    disks = {}
    for partition in psutil.disk_partitions(all=False):
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            total_gb = usage.total / (1024 ** 3)
            used_gb = usage.used / (1024 ** 3)
            free_gb = usage.free / (1024 ** 3)
            disks[partition.device] = (
                f"{used_gb:.1f} GB / {total_gb:.1f} GB used "
                f"({usage.percent}% full) | Free: {free_gb:.1f} GB"
            )
        except PermissionError:
            # Skip optical drives or restricted partitions
            continue
    return disks

def gather_detailed_info():
    """Gathers combined OS, network, RAM, and Disk metrics."""
    # RAM statistics
    ram = psutil.virtual_memory()
    total_ram_gb = ram.total / (1024 ** 3)
    available_ram_gb = ram.available / (1024 ** 3)

    return {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Hostname": socket.gethostname(),
        "Operating System": f"{platform.system()} {platform.release()} ({platform.machine()})",
        "Public IP": get_public_ip(),
        "CPU Cores": f"{psutil.cpu_count(logical=False)} Physical / {psutil.cpu_count(logical=True)} Logical",
        "Total RAM": f"{total_ram_gb:.2f} GB (Available: {available_ram_gb:.2f} GB | Usage: {ram.percent}%)",
        "Disk Usage": get_disk_usage(),
        "Network Interfaces": get_network_interfaces()
    }

def log_system_info(filename="detailed_system_log.txt"):
    """Formats and writes system details to stdout and log file."""
    data = gather_detailed_info()
    
    log_entry = "==========================================================\n"
    log_entry += f" SYSTEM DIAGNOSTIC LOG - {data['Timestamp']}\n"
    log_entry += "==========================================================\n"
    
    for key, value in data.items():
        if isinstance(value, dict):
            log_entry += f"\n[{key}]\n"
            for sub_key, sub_val in value.items():
                log_entry += f"  - {sub_key:<20}: {sub_val}\n"
        else:
            log_entry += f"{key:<20}: {value}\n"
            
    log_entry += "==========================================================\n\n"
 
    # Console display
    print(log_entry)

    # Append entry to log file
    with open(filename, "a", encoding="utf-8") as f:
        f.write(log_entry)
        
    print(f"[+] Diagnostic report saved to '{os.path.abspath(filename)}'")

if __name__ == "__main__":
    log_system_info()