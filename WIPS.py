import socket
from threading import Thread
import threading
import os
HOST = ""
##HOST = socket.gethostbyname(socket.gethostname()) 
print(socket.gethostname())
PORT = 8080
clients = set()
clientLock = threading.Lock()
def on_new_client(cs, addr):
    cs.send(b"What is the username? ")
    username = cs.recv(1024).decode()
    cs.send(b"""Welcome to SimplexChat!
To quit just type in quit()
Have fun communcating!
""")
    spam == 0
    while True:
        data = cs.recv(1024).decode()
        if data == "":
            print("User has put in a blank")
            spam = spam + 1
            if spam == 5:
                cs.send(b"""You have put in a blank 5 times.
Due to our spam policy we must disconnect you.
You are able to reconnect.
Good Bye.""")
                break
        if data == "quit()":
            break
        with clientLock:
            data = "User:" + username + "> " + data
            for c in clients:
                c.sendall(data.encode())
    cs.close()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))

s.listen()
while True:
    conn, addr = s.accept()
    with clientLock:
        clients.add(conn)
    print("New connection from {addr}" )
    thread = Thread(target=on_new_client, args=(conn, addr))
    thread.start()
    
conn.close()
thread.join()        


