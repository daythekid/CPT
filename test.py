import socket

HOST = '192.168.0.21'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket:
    socket.bind((HOST, PORT))
    socket.listen()
    conn, addr = socket.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            conn.