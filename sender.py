import os
import socket

# Prompt user for file path and destination filename
file_path = input("Enter the path to the file to send: ")
dest_filename = input("Enter the destination filename: ")

if not os.path.isfile(file_path):
    print(f"File '{file_path}' does not exist.")
    exit(1)

file_size = os.path.getsize(file_path)

try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 9999))

    # Send filename and filesize, each followed by a newline
    client.sendall((dest_filename + '\n').encode())
    client.sendall((str(file_size) + '\n').encode())

    with open(file_path, 'rb') as file:
        while True:
            data = file.read(1024)
            if not data:
                break
            client.sendall(data)
    print(f"File '{file_path}' sent successfully as '{dest_filename}'.")
    client.close()
except Exception as e:
    print(f"Error: {e}")