import socket
HOST = input()
PORT =11111
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((HOST,PORT))
while 1:
    keyin=input()
    client.send(str.encode(keyin))