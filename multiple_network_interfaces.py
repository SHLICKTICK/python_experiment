import socket
import psutil

def get_status_str(is_up):
    return "UP [Active]" if is_up else "DOWN [Inactive]"

def list_network_interfaces():
    interfaces = psutil.net_if_addrs()
    interface_stats = psutil.net_if_stats()

    print("==========================================================================")
    print("                      AVAILABLE NETWORK INTERFACES                        ")
    print("==========================================================================")

    for iface_name, addresses in interfaces.items():
        # Retrieve hardware status (Up/Down, Speed)
        stats = interface_stats.get(iface_name)
        status = get_status_str(stats.isup) if stats else "UNKNOWN"
        speed = f"{stats.speed} Mbps" if stats and stats.speed > 0 else "N/A"

        print(f"\n[Interface]: {iface_name}")
        print(f"  Status : {status}")
        print(f"  Speed  : {speed}")
        print("  Addresses:")

        for addr in addresses:
            # Check address family
            if addr.family == socket.AF_INET:
                print(f"    - IPv4 Address : {addr.address}")
                if addr.netmask:
                    print(f"      Subnet Mask  : {addr.netmask}")
            elif addr.family == socket.AF_INET6:
                # Strip scope ID from link-local IPv6 addresses if present
                clean_ipv6 = addr.address.split('%')[0]
                print(f"    - IPv6 Address : {clean_ipv6}")
            elif addr.family == getattr(psutil, 'AF_LINK', None) or addr.family == getattr(socket, 'AF_LINK', -1):
                print(f"    - MAC Address  : {addr.address}")

    print("\n==========================================================================")

if __name__ == "__main__":
    list_network_interfaces()