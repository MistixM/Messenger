# Server script

"""
    Server for multithreaded chat application

    We'll be using TCP instead of UDP sockets, because of TCP sockers are more telephonic.

    NOTICE! If server don't launch and raise 'PermissionError: [WinError 10013]' just 
    reboot network system.
    Using: 'net stop hns; net start hns' command in powershell (with admin permissions)
"""

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import customtkinter # Should be installed
from tkinter import messagebox
from PIL import Image # Should be installed
import time


def get_status(s):
    return s

def main():
    global SERVER, BUFSIZ, ACCEPT_THREAD, addresses, clients, app, status

    clients = {}
    addresses = {}
    
    # Initialisate ui engine
    app = customtkinter.CTk()

    HOST = ''
    PORT = 2424
    BUFSIZ = 1024
    status = True
    print(get_status(status))

    ADDR = (HOST, PORT)
    SERVER = socket(AF_INET, SOCK_STREAM)
    SERVER.bind(ADDR)
    SERVER.listen()

    print("Waiting for connection..")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)

    ACCEPT_THREAD.start() # Start the loop
    draw_ui()
    
    ACCEPT_THREAD.join() # Main script should waits for Thread complete and doesn't jump to next line
    SERVER.close()

def draw_ui():
    global logs

    def on_closing(event=None):
        global status
        confirm = messagebox.askyesno("Server shutdown","This action will cause the server to stop. Are you sure?")
        
        if confirm:
            for client in clients:
                client.send(bytes("SHUTDOWN", "utf-8"))

            app.destroy()
            status = False
            
            SERVER.close()
            print("Server was closed")

        return on_closing

    app.geometry("600x300")
    app.resizable(False, False)
    app.title("Server launcher")
 
    # Contain log messages

    logs = customtkinter.CTkScrollableFrame(app, height=200, width=550)
    logs.pack(side=customtkinter.BOTTOM, pady=10)
    
    start_msg = customtkinter.CTkLabel(logs, 
                                       height=10, 
                                       width=logs.cget("width"), 
                                       anchor="nw", 
                                       text=f"{time.strftime('%H:%M:%S', time.localtime())} - Waiting for connection.."
                                       )
    start_msg.pack()

    # Buttons
    stop_server = customtkinter.CTkButton(app, 
                                          width=30, 
                                          height=30, 
                                          text="", 
                                          image=customtkinter.CTkImage(dark_image=Image.open("project/power.png"), 
                                          size=(20, 20)), 
                                          command=on_closing, 
                                          fg_color="#FFFFFF", 
                                          hover_color="#F0F0F0"
                                          )
    
    stop_server.pack(side="left", anchor="s", padx=12)
    app.protocol("WM_DELETE_WINDOW", on_closing)

    app.mainloop()

def accept_incoming_connections():
    # Setup handling for incoming clients..
    global client_address
    while status:
        try:
            client, client_address = SERVER.accept()
        except OSError:
            break
            
        
        info = customtkinter.CTkLabel(logs, 
                                      height=0, 
                                      width=logs.cget("width"), 
                                      anchor="nw", 
                                      text=f"{time.strftime('%H:%M:%S', time.localtime())} - {client_address} has connected."
                                      )
        info.pack()
        # client.send(bytes("Server: Greetings!" + "Type your name and press enter!", "utf-8"))
        addresses[client] = client_address

        Thread(target=handle_client, args=(client,)).start()
    
def handle_client(client): # Takes client socket as arg
    # Handles a single client connection..

    name = client.recv(BUFSIZ).decode("utf-8")
    welcome = f'Server: Welcome {name}! If you ever want to quit, type "quit" to exit the program.'
    try:
        client.send(bytes(welcome, "utf-8"))
    except ConnectionResetError:
        client.close()

    msg = f"{name} has joined the chat."
    broadcast(bytes(msg, "utf-8"))
    clients[client] = name

    while True:
        try:
            msg = client.recv(BUFSIZ)
        except (ConnectionResetError, OSError):
            client.close()
            del clients[client]
            broadcast(bytes(f"{name} has left the chat.", "utf-8"))
            break

        if msg != bytes("/quit", "utf-8"):
            broadcast(msg, name + ": ")
    
        else:
            try:
                client.send(bytes("/quit", "utf-8"))
            except ConnectionResetError:
                client.close()
                del clients[client]
                broadcast(bytes(f"{name} has left the chat.", "utf-8"))
                info = customtkinter.CTkLabel(logs, 
                                              height=0, 
                                              width=logs.cget("width"), 
                                              anchor="nw", 
                                              text=f"{time.strftime('%H:%M:%S', time.localtime())} - User: {name} with {client_address} has left the server!"
                                              )
                
                info.pack()
                break
            if msg:
                name = msg.decode("utf-8")[5:]
            elif msg != bytes("/quit", "utf-8"):
                broadcast(msg, name + ": ")


def broadcast(msg, prefix=""): # prefix needs for name identification
    # Broadcast a message to all clients.
    for sock in clients:
        try:
            sock.send(bytes(prefix, "utf-8") + msg)
        except OSError:
            del clients[sock]

if __name__ == "__main__": 
    main()