from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import customtkinter
import tkinter

from PIL import Image
from tkinter import messagebox

def get_receive(state):
    if state:
        return True
    else:
        return False

def check_gui(size, name):
    if size is not None and name is not None:
        return True
    else:
        return False
    
def main():
    global client_socket, can_receive, app, BUFSIZ, ADDR

    app = customtkinter.CTk()
    app.title("Join chat")
    app.geometry("378x356")
    app.resizable(False, False)

    can_receive = False

    def connect():
        global client_socket, can_receive, BUFSIZ

        HOST = server_ip.get()
        PORT = server_port.get()

        if not PORT:
            PORT = 2424
        else:
            PORT = int(PORT)

        BUFSIZ = 1024
        ADDR = (HOST, PORT)

        client_socket = socket(AF_INET, SOCK_STREAM)

        try:
            client_socket.connect(ADDR)
        except ConnectionRefusedError:
            messagebox.showerror("Client", "The connection has been lost!")
        except OSError:
            messagebox.showerror("Client", "Invalid data! Please, re-check your port and ip!")
        if not name_entry.get():
            messagebox.showerror("Client", "Invalid name!")
        else:
            client_socket.send(bytes(name_entry.get(), "utf-8"))
            can_receive = True

            registration_frame.destroy()

            draw_ui()

    # Registration form
    registration_frame = customtkinter.CTkFrame(app, width=600, height=600)
    registration_frame.pack(expand=True, fill='both')

    field_frame = customtkinter.CTkFrame(registration_frame, width=120, height=120, fg_color="#424242")
    field_frame.pack(expand=True, fill='y', pady=80)

    name_entry = customtkinter.CTkEntry(field_frame, width=150, height=10, placeholder_text="Name")
    name_entry.pack(pady=5)

    server_ip = customtkinter.CTkEntry(field_frame, width=150, height=10, placeholder_text="Server IP")
    server_ip.pack(pady=5)

    server_port = customtkinter.CTkEntry(field_frame, width=150, height=10, placeholder_text="Server Port: 2424")
    server_port.pack(pady=5)

    connect_button = customtkinter.CTkButton(field_frame, width=100, height=10, text="Join!", command=connect)
    connect_button.pack(pady=35)

    app.mainloop()

def draw_ui():
    def receive():
        # Handles receiving of messages
        while can_receive:
            try:
                msg = client_socket.recv(BUFSIZ).decode("utf-8")
                if msg == "SHUTDOWN":
                    client_socket.close()
                    app.quit()
                    messagebox.showerror("Client", "The connection has been lost!")
                    break
                text_msg = customtkinter.CTkLabel(message_frame, width=message_frame.cget("width"), height=20, text=msg, anchor='nw')
                text_msg.pack()
            except OSError:
                break

    def send(event=None):
        # Handles sending of messages

        msg = my_msg.get()
        my_msg.set("")
        client_socket.send(bytes(msg, "utf-8"))
        if msg == "/quit":
            client_socket.close()
            app.quit()

    def on_closing(event=None):
        # This function will be called when the window is closed
        my_msg.set("/quit")
        send()

    app.geometry("600x600")
    app.title("Chat")

    message_frame = customtkinter.CTkScrollableFrame(app, width=600, height=540)
    message_frame.pack(side='top')

    my_msg = tkinter.StringVar()  # For message sent

    entry_msg = customtkinter.CTkEntry(app, placeholder_text="Write message...", textvariable=my_msg, width=550, height=50)
    entry_msg.pack(side="bottom", anchor='sw')
    entry_msg.bind("<Return>", send)

    _send = customtkinter.CTkButton(app, text="", image=customtkinter.CTkImage(dark_image=Image.open("project/send.png"), size=(30, 30)), command=send, width=40, height=40)
    _send.pack_forget()
    _send.place(relx=0.92, rely=0.928)

    receive_thread = Thread(target=receive)
    print("receving")
    app.protocol("WM_DELETE_WINDOW", on_closing)
    receive_thread.start()

if __name__ == "__main__":
    main()
