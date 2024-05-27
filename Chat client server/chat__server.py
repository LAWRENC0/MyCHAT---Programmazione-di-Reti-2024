#!/usr/bin/env python3

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

#thread made for accepting new clients
def accept_manager():
    print("SERVER attivo. In attesa di CLIENTs...")
    while True:
        CLIENT_SOCKET, CLIENT_ADDR = SERVER_SOCKET.accept()
        CLIENT_THREAD = Thread(target=client_manager, args=(CLIENT_SOCKET, CLIENT_ADDR))
        CLIENT_THREAD.start()

#thread made for managing each client independently
def client_manager(client_socket, client_addr):
    try:
        print("Accesso di un nuovo client: %s:%s" % client_addr)

        client_socket.send(bytes("Benvenuto! Inserisci il tuo nome e premi INVIO!", "utf8"))
        client_name = client_socket.recv(BUFFER_SIZE).decode("utf8")
        #make sure each client has a different username
        while client_name in client_names.values():
            client_socket.send(bytes("Questo nome è già in uso. Prova con un altro!", "utf8"))
            client_name = client_socket.recv(BUFFER_SIZE).decode("utf8")
        client_names[client_socket] = client_name
        client_socket.send(bytes("Hey " + client_name + "! Per uscire, digita " + CLIENT_QUIT_MESSAGE, "utf8"))
        
        msg = "Utente %s si è unito alla chat." % client_name
        broadcast(msg, SERVER_NAME)
        #this is the main "chat loop". clients send and receive messages here
        try:
            while True:
                msg = client_socket.recv(BUFFER_SIZE).decode("utf8")
                if msg != CLIENT_QUIT_MESSAGE:
                    broadcast(msg, client_name)
                else:
                    break
        except OSError:
            print(client_name + " ha lasciato la chat")
        finally:
            client_quit(client_name, client_socket)
    except OSError:
        msg = "%s:%s non si è unito alla chat" % client_addr
        print(msg)
        broadcast(msg, SERVER_NAME)
    return

#when receiving a message from a client, we want to share it with every other client
def broadcast(msg, prefix=""):
    if client_names:
        for client_socket in client_names:
            client_socket.send(bytes(prefix + ": " +  msg, "utf8"))

#manage a client quit
def client_quit(client_name, CLIENT_SOCKET):
    msg = "Utente %s ha lasciato la chat." % client_name
    CLIENT_SOCKET.close()
    del client_names[CLIENT_SOCKET]
    broadcast(msg, SERVER_NAME)

HOST = 'localhost'
PORT = 8080
ADDR = (HOST, PORT)
BUFFER_SIZE = 1024
client_names = {}

CLIENT_QUIT_MESSAGE = "{quit}"
SERVER_NAME = "SERVER"

SERVER_SOCKET = socket(AF_INET, SOCK_STREAM)
SERVER_SOCKET.bind(ADDR)

if __name__ == '__main__':
    try:
        #open our socket to enque clients
        SERVER_SOCKET.listen(5)
        ACCEPT_THREAD = Thread(target=accept_manager)
        #start the thread for accepting new clients
        ACCEPT_THREAD.start()
        ACCEPT_THREAD.join()
    finally:
        #make sure we close our socket
        SERVER_SOCKET.close()



