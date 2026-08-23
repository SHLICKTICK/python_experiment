import socket
import psutil

def format_bytes(bytes_num):
    """Converts raw byte counts into human-readable units (KB, MB, GB)."""
    if bytes_num >= 1024 ** 3:
        return f"{bytes_num / (1024 ** 3):.2f} GB"
    elif bytes_num >= 1024 ** 2:
        return f"{bytes_num / (1024 ** 2):.2f} MB"
    elif bytes_num >= 1024:
        return f"{bytes_num / 1024:.2f} KB"
    return f"{bytes_num} Bytes"

def get_status_str(is_up):
    return "UP [Active]" if is_up else "DOWN [Inactive]"

def list_detailed_interfaces():
    interfaces = psutil.net_if_addrs()
    interface_stats = psutil.net_if_stats()
    # pernic=True returns network IO statistics isolated per individual card
    io_counters = psutil.net_io_counters(pernic=True)

    print("==========================================================================")
    print("              NETWORK INTERFACES & TRAFFIC STATISTICS                     ")
    print("==========================================================================")

    for iface_name, addresses in interfaces.items():
        stats = interface_stats.get(iface_name)
        status = get_status_str(stats.isup) if stats else "UNKNOWN"
        speed = f"{stats.speed} Mbps" if stats and stats.speed > 0 else "N/A"

        print(f"\n[Interface]: {iface_name}")
        print(f"  Operational Status : {status}")
        print(f"  Link Speed         : {speed}")

        # 1. Address Details
        print("  Addresses:")
        for addr in addresses:
            if addr.family == socket.AF_INET:
                print(f"    - IPv4 Address   : {addr.address}")
                if addr.netmask:
                    print(f"      Subnet Mask    : {addr.netmask}")
            elif addr.family == socket.AF_INET6:
                clean_ipv6 = addr.address.split('%')[0]
                print(f"    - IPv6 Address   : {clean_ipv6}")
            elif addr.family == getattr(psutil, 'AF_LINK', None) or addr.family == getattr(socket, 'AF_LINK', -1):
                print(f"    - MAC Address    : {addr.address}")

        # 2. Traffic & Packet Statistics
        if iface_name in io_counters:
            io = io_counters[iface_name]
            print("  Traffic Counters:")
            print(f"    - Bytes Transferred : Sent: {format_bytes(io.bytes_sent):<12} | Recv: {format_bytes(io.bytes_recv)}")
            print(f"    - Total Packets     : Sent: {io.packets_sent:<12,} | Recv: {io.packets_recv:,}")
            print(f"    - Errors & Drops    : Errors: {io.errin + io.errout:<10} | Dropped: {io.dropin + io.dropout}")
        else:
            print("  Traffic Counters: Unavailable")

        print("  " + "-" * 68)

    print("\n==========================================================================")

if __name__ == "__main__":
    list_detailed_interfaces()