#!/usr/bin/env python3

from socket import AF_INET, socket, SOCK_STREAM
import tkinter as tkt
import tkinter.font
from threading import Thread
import sys

def receive_message():
    try:
        print("Application started!")
        while True:
            #socket waits for messages
            new_msg = MY_SOCKET.recv(BUFFER_SIZE).decode("utf8")
            if not new_msg:
                break
            #add received message to message list
            MSG_LIST.insert(tkt.END, new_msg)
    except OSError:
        print("Application closed!")
    finally:
        MY_SOCKET.close()
        WINDOW.quit()
    return

def send_message(event=None):
    new_msg = MY_MSG.get()
    MY_MSG.set("")
    #what to do in case the client wants to quit
    if new_msg == "{quit}":
        MY_SOCKET.close()
        WINDOW.quit()
        return
    #what to do for a generic message
    if new_msg:
        MY_SOCKET.send(bytes(new_msg, "utf8"))

def on_close(event=None):
    #send a quit message in every instance of application closing
    MY_MSG.set("{quit}")
    send_message()

#this function creates the GUI
def window_creation():
    WINDOW = tkt.Tk()
    WINDOW.title("MyCHAT")
    WINDOW.configure(bg="firebrick4")
    default_font = tkinter.font.Font(family="Calibri Light", size=13)
    title_font = tkinter.font.Font(family="Papyrus", size=20)

    TOP_FRAME = tkt.Frame(WINDOW, bg="burlywood1")
    TOP_FRAME.pack(pady=15)

    MESSAGE_FRAME = tkt.Frame(WINDOW, bg="burlywood1")
    MY_MSG = tkt.StringVar()
    MY_MSG.set("Scrivi qui i tuoi messaggi.")

    TITLE = tkt.Label(TOP_FRAME, text="MyCHAT", font=title_font, bg="sandy brown", fg="black")
    TITLE.pack()

    SCROLLBAR = tkt.Scrollbar(MESSAGE_FRAME)

    MSG_LIST = tkt.Listbox(MESSAGE_FRAME, height=15, width=50, yscrollcommand=SCROLLBAR.set, font="default_font", bg="orange2", fg="black")
    SCROLLBAR.pack(side=tkt.RIGHT, fill=tkt.Y)
    MSG_LIST.pack(side=tkt.LEFT, fill=tkt.BOTH)
    MSG_LIST.pack()
    MESSAGE_FRAME.pack()

    ENTRY_FIELD = tkt.Entry(WINDOW, textvariable=MY_MSG, width=40, font=default_font, bg="firebrick2", fg="black")
    ENTRY_FIELD.bind("<Return>", send_message)

    ENTRY_FIELD.pack()
    SEND_BUTTON = tkt.Button(WINDOW, text="SEND", command=send_message, font=default_font, bg="IndianRed3", fg="black")
    SEND_BUTTON.pack()

    WINDOW.protocol("WM_DELETE_WINDOW", on_close)

    return WINDOW, MSG_LIST, MY_MSG

if __name__ == "__main__":
    try:
        #take the server address as input
        try:
            HOST = input("Type the address of the server: ")
        except KeyboardInterrupt:
            sys.exit(0)
        PORT = 8080
        ADDR = (HOST, PORT)
        BUFFER_SIZE = 1024

        MY_SOCKET = socket(AF_INET, SOCK_STREAM)
        MY_SOCKET.connect(ADDR)

        WINDOW, MSG_LIST, MY_MSG = window_creation()
        RECEIVE_THREAD = Thread(target=receive_message, daemon=True)
        RECEIVE_THREAD.start()

        tkt.mainloop()
        RECEIVE_THREAD.join()
    except OSError:
        print("Something went wrong...")
    finally: 
        MY_SOCKET.close()
