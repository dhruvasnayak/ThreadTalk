import socket
import ssl
import threading

HOST = '0.0.0.0'
PORT = 8080

def handle_client(conn, addr):
    
    while True:
        try:
            message = conn.recv(1024).decode('utf-8')
            print(message)
            arr = message.split(':')
            username = arr[0]
            room = arr[1]
            msg = arr[2]
            message=""+username+":"+msg

            if conn not in clidict:
                clidict[conn] = room
            else:
                room = clidict[conn]
                for sock, sock_room in clidict.items():
                    if sock_room == room and sock!=conn:
                        sock.send(message.encode())
        except:
            index = clients.index(conn)
            clients.remove(conn)
            clidict.pop(conn, None)
            conn.close()
            print(f"Connection closed: {addr}")
            break


def start_server():
    ssl_socket.listen()

    while True:
        conn, addr = ssl_socket.accept()
        clients.append(conn)
        iparr.append(addr)

        print("current users in the chat")
        j=0
        for i in iparr:
             j+=1
             print(f"Client {j}: {i}")
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


clients = []
clidict = dict()
iparr=[]

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, 8080))

certfile = "server.crt"
keyfile = "server.key"
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(certfile, keyfile)
ssl_socket = ssl_context.wrap_socket(server_socket, server_side=True)

if __name__ == "__main__":
    start_server()