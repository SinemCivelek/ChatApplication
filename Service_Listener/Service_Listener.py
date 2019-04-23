import socket
import select

HEADER_LENGHT = 10
IP = "192.168.44.1"
PORT = 5000

print("Service Listener")

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('',PORT)) 
serversocket.listen(1)

while True:
    conn, addr = serversocket.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
