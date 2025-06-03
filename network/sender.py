"""
File Sender - Handles sending files over network
"""

import socket
import os
from utils.helpers import discover_file_server_ip

class FileSender:
    def __init__(self):
        pass

    def send_file(self, file_path, host, port, dest_filename, progress_callback=None, auto_discover=True):
        """
        Send a file to a remote host
        
        Args:
            file_path: Path to the file to send
            host: Target host address (or 'auto' to use discovery)
            port: Target port number
            dest_filename: Filename to save as on receiver
            progress_callback: Function to call with progress updates (0-100)
            auto_discover: If True and host is 'auto', use UDP broadcast to find server
        """

        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"File '{file_path}' does not exist.")

        file_size = os.path.getsize(file_path)

        # Auto-discover host if requested
        if auto_discover and (host == 'auto' or not host or host.strip() == ''):
            host = discover_file_server_ip()

        # Create socket and connect to the server
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))

        try:
            # Send filename and filesize
            client.sendall((dest_filename + '\n').encode())
            client.sendall((str(file_size) + '\n').encode())

            # Send file data
            with open(file_path, 'rb') as file:
                sent = 0
                while True:
                    data = file.read(1024)
                    if not data:
                        break
                    client.sendall(data)
                    sent += len(data)

                    # Update progress if callback is provided
                    if progress_callback:
                        progress = (sent / file_size) * 100
                        progress_callback(progress)
        
        finally:
            client.close()