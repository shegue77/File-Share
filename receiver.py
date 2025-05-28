import socket
import tqdm


def recv_line(sock):
    line = b""
    while True:
        char = sock.recv(1)
        if char == b"\n" or char == b"":
            break
        line += char
    return line.decode()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9999))
server.listen()

client, addr = server.accept()

file_name = recv_line(client)
print(file_name)
file_size = int(recv_line(client))
print(file_size)


file = open(file_name, "wb")

progress = tqdm.tqdm(unit="B", unit_scale=True, unit_divisor=1000, total=file_size)
received = 0

while received < file_size:
    data = client.recv(1024)
    if not data:
        break
    file.write(data)
    received += len(data)
    progress.update(len(data))

file.close()
client.close()
server.close()
