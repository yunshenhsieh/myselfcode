import socket
# server的HOST就是自己的IP
HOST=''
PORT=11111

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((HOST,PORT))
server.listen()
client , adress = server.accept()
while 1:
    print(client.recv(1024).decode())