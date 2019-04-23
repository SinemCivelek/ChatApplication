import socket
import select

HEADER_LENGHT = 10
IP = "192.168.44.1"
PORT = 5000

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
server.bind((IP,PORT))
server.listen()
sockets_list = [server]

clients = {}


def msg(client_socket):
    try:
        msg_header = client_socket.recv(HEADER_LENGHT)
        if not len(msg_header):
            return False
        msg_length = int(msg_header.decode('utf8').strip())
        return {"header":msg_header,"data":client_socket.recv(msg_length)}
    except:
     return False

while True:
    read_sockets,_,exeption_sockets = select.select(sockets_list,[],sockets_list)

    for notified_socket in read_sockets :
        if notified_socket == server:
            client_socket, client_address = server.accept()
            user = msg(client_socket)

            if user is False: 
               continue

            sockets_list.append(client_socket)
            clients[client_socket] = user
            print(f"Accepted new connection from {client_address[0]}:{client_address[1]} username:{user['data'].decode('utf-8')}")
        else:
            message = msg(notified_socket)
            if message is False:
                 print(f"Closed connection from {clients[notified_socket]['data'].decode('utf-8')}")
                 sockets_list.remove(notified_socket)
                 del clients[client_socket]
                 continue
            
            user = clients[notified_socket]
            print(f"Recieved message from {user['data'].decode('utf-8')}:{message['data'].decode('utf+8')}")

            for client_socket in clients:
                if client_socket != notified_socket:
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

    for notified_socket in exeption_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]
          












