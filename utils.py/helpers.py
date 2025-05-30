"""
Helper Functions - Common utilities
"""

import os
import socket

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