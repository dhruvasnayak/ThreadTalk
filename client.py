import socket
import threading
import tkinter as tk
import ssl

HOST = '127.0.0.1'
PORT = 8080

class Room:
    def __init__(self):
        certfile = "server.crt"
        ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        ssl_context.load_verify_locations(certfile)

        server_address = (HOST, 8080)
        self.client_socket = ssl_context.wrap_socket(socket.socket(socket.AF_INET), server_hostname='localhost')
        self.client_socket.connect(server_address)
        
        self.root = tk.Tk()
        self.root.title("Chat Room")
        
        self.username_frame = tk.Frame(self.root)
        self.username_frame.pack(padx=10, pady=10)
        self.username_label = tk.Label(self.username_frame, text="Username: ")
        self.username_label.pack(side=tk.LEFT)
        self.username_entry = tk.Entry(self.username_frame, width=50)
        self.username_entry.pack(side=tk.LEFT)

        self.room_frame = tk.Frame(self.root)
        self.room_frame.pack(padx=10, pady=10)
        self.room_label = tk.Label(self.room_frame, text="Roomname: ")
        self.room_label.pack(side=tk.LEFT)
        self.room_entry = tk.Entry(self.room_frame, width=50)
        self.room_entry.pack(side=tk.LEFT)
       
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(padx=10, pady=10)
        self.button = tk.Button(self.button_frame, text="message", command=self.send_message)
        self.button.pack()

        self.root.mainloop()


    def send_message(self):
        username = self.username_entry.get()
        room = self.room_entry.get()

        if username and room:
            full_message = f"{username}: {room}:"
            self.client_socket.send(full_message.encode())
            
            self.root.destroy()
            ChatClient(self.client_socket, username, room)

class ChatClient:
    def __init__(self, client_socket, username, room):
        
        self.client_socket = client_socket
        self.username = username
        self.room = room

        self.root2 = tk.Tk()
        self.root2.title("Chat Room")

        self.chat_frame = tk.Frame(self.root2,bg="#FF00FF")
        self.chat_frame.pack(padx=10, pady=10)

        self.chat_scrollbar = tk.Scrollbar(self.chat_frame)
        self.chat_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.chat_text = tk.Text(self.chat_frame, height=20, width=50, yscrollcommand=self.chat_scrollbar.set)
        self.chat_text.pack(side=tk.LEFT, fill=tk.BOTH)
        self.chat_scrollbar.config(command=self.chat_text.yview)

        self.message_frame = tk.Frame(self.root2)
        self.message_frame.pack(padx=10, pady=10)

        self.message_label = tk.Label(self.message_frame, text="Message: ")
        self.message_label.pack(side=tk.LEFT)

        self.message_entry = tk.Entry(self.message_frame, width=50)
        self.message_entry.pack(side=tk.LEFT)

        self.send_button = tk.Button(self.message_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.LEFT)

        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()

        self.root2.mainloop()

    def send_message(self):
    
        username = self.username
        room = self.room
        message = self.message_entry.get()

        if username and message:
            self.message_entry.delete(0, tk.END)
            full_message = f"{username}:{room}:{message}"
            self.chat_text.tag_configure("right", justify="right")
            self.chat_text.insert(tk.END, message + "\n", "right")
            self.client_socket.send(full_message.encode())

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode()
                self.chat_text.insert(tk.END, message+"\n")
                self.chat_text.see(tk.END)
            except:
                self.client_socket.close()
                break

if __name__ == "__main__":
    Room()