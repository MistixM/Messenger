# Messenger

## Description:
A simple messenger that will help you communicate between people or just have a discussion. The messenger is also quite easy to use and the interface is easy to understand.

## Implementation Details
This project uses the socket library to ensure proper operation of the server and client, as well as proper processing of data between them. Also, customtkinter is used for a more modern and simple interface design. Multithreading is also implemented using the Thread library. PIL for image processing.

The script uses a TCP connection instead of UDP because TCP is more telephonic and you need to wait until the second user accepts the connection before sending the message. In the future, I will try to implement a UDP connection. Also, in the future (possibly) connection to a single server will be implemented.

Briefly about functions. The server script has a main() function that draws and sends data to the server from the client draw_ui() draws the main server interface (also, a debug log was implemented in the interface to obtain information about the chat)

accept_incoming_connections() this function is responsible for connecting users to the server and processing their data handle_client() is responsible for handling client data, naming, and sending and displaying correctly on the client side

broadcast() is responsible for sending messages

Briefly about the functions in the client script. The main() function handles the interface and other functions that will work in the future. The internal function connect() is responsible for checking the entered data from the user, as well as the correct transformation of the ui after the correct data. draw_ui() draws the chat itself and all the elements in it. Also, internal functions are responsible for the functionality of sending and receiving messages and, in principle, communication with the server.

## How to Run
Before you start chat: -1- Make sure you have your operating system's firewall and antivirus disabled. Sometimes the program conflicted with these restrictions and this caused errors.

To start a chat (if you are a regular user): -1- Open client.py (or client.exe if the program has already been released) -2- Enter the required data in the fields (name, ip, port). It is not necessary to enter the port. -3- Click Join and if there are no errors, you will be allowed into the chat.

To start a chat (if you are the host): -1- Run server.py (or server.exe if the program was released) -2- After launch, you need to find out your machine IP and send it to the second user -3- If method 2 does not work, then use Radmin VPN.

## Addition message
Unfortunately, so far connecting the program sometimes does not work correctly, but I am trying to find a way to connect to a single server. It just takes more experience and time to solve this problem.