"""
Helper Functions - Common utilities
"""

import os
import socket
import time

def format_file_size(size_bytes):
    """
    Format file size in human readable format
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted string (e.g., "1.5 MB")
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024.0 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"

def validate_port(port_str):
    """
    Validate port number
    
    Args:
        port_str: Port as string
        
    Returns:
        Port as integer if valid, raises ValueError if invalid
    """
    try:
        port = int(port_str)
        if not (1 <= port <= 65535):
            raise ValueError("Port must be between 1 and 65535")
        return port
    except ValueError:
        raise ValueError("Invalid port number")

def is_port_available(host, port):
    """
    Check if a port is available
    
    Args:
        host: Host address
        port: Port number
        
    Returns:
        True if port is available, False otherwise
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, port))
        return True
    except:
        return False

def safe_filename(filename):
    """
    Create a safe filename by removing/replacing invalid characters
    
    Args:
        filename: Original filename
        
    Returns:
        Safe filename
    """
    # Characters that are not allowed in filenames
    invalid_chars = '<>:"/\\|?*'
    
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Remove leading/trailing dots and spaces
    filename = filename.strip('. ')
    
    # Ensure filename is not empty
    if not filename:
        filename = "unnamed_file"
        
    return filename

def get_local_ip():
    """
    Get the local IP address of the machine
    
    Returns:
        Local IP address as string
    """
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # Doesn't matter if 8.8.8.8 is reachable or not, we just need a valid address
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1" # Fallback to localhost if unable to determine IP
    finally:
        s.close()
    
    return ip

def discover_file_server_ip(broadcast_port=37020, timeout=2):
    """
    Discover file server IP on the local network using UDP broadcast.
    Returns the discovered IP address as a string, or None if not found.
    """
    message = b"DISCOVER_FILE_SERVER"
    server_ip = None
    attempts = ["<broadcast>", "192.168.1.255"]  # fallback strategy
    
    # Set up UDP socket for broadcast
    for attempt in attempts:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            s.settimeout(timeout)
            try:
                s.sendto(message, (attempt, broadcast_port))
                # Wait for a response
                server_ip, _ = s.recvfrom(1024)
                server_ip = server_ip.decode()
                break
            except socket.timeout:
                continue
            except Exception:
                # No response, do not fallback to local IP
                print(f"[DEBUG] Discovery attempt to {attempt} failed: {e}")
                server_ip = None

    return server_ip