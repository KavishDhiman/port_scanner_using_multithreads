import pyfiglet
import socket
import threading
from datetime import datetime
import ipaddress

# Display banner
ascii_banner = pyfiglet.figlet_format("PORT SCANNER")
print(ascii_banner)

# Function to validate IP
def validate_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

# Get target IP
while True:
    target = input("Enter Target IP: ").strip()
    if validate_ip(target):
        break
    else:
        print("❌ Invalid IP address! Please enter a valid IP.")

# Print scan details
print("\n" + "*" * 50)
print(f"Scanning Target: {target}")
print(f"Scanning started at: {datetime.now()}")
print("*" * 50)

# Function to scan a port
def scan_port(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)  # Reduce timeout for faster scanning
        result = s.connect_ex((target, port))
        if result == 0:
            print(f"✅ Port {port} is OPEN!")
        s.close()
    except (socket.timeout, socket.error):
        pass

# Using multithreading for faster scanning
def start_scan(start_port, end_port, thread_count=100):
    threads = []
    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=scan_port, args=(port,))
        thread.start()
        threads.append(thread)

        # Limit active threads to avoid overload
        if len(threads) >= thread_count:
            for t in threads:
                t.join()  # Wait for all threads to complete
            threads = []  # Reset thread list

    # Wait for remaining threads to finish
    for t in threads:
        t.join()

# Run the scanner (Scanning first 1024 ports)
start_scan(1, 1024, thread_count=200)

print("\n✅ Scan completed!")
