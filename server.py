import threading
import socket
import argparse
import os
import json
import time

DATA_PATH = "data.json"
usernames = [ "ada", "badut", "makoto", "jokowi", "28", "fut", "donkey", "vegito", "suki", "queen", "croc", "faisal", "ex fbk", "ntr" ]

class Server (threading.Thread):
    def __init__(self, host, port):        
        super().__init__()
        self.connections = []
        self.host = host
        self.port = port
        
        with open(DATA_PATH) as f:
            self.data = json.load(f)

    def run(self):
        sock = socket.socket(
            socket.AF_INET, 
            socket.SOCK_STREAM
        )
        sock.setsockopt(
            socket.SOL_SOCKET, 
            socket.SO_REUSEADDR,
            1
        )
        sock.bind((self.host, self.port))
        sock.listen(1)

        print("Listening at", sock.getsockname())

        while (True):
            # Accept new connection
            sc, sockname = sock.accept()
            print(f"{sc.getpeername()} connecting to {sc.getsockname()}")

            # Create new thread
            server_socket = ServerSocket(sc, sockname, self)

            # start new thread
            server_socket.start()

            self.connections.append(server_socket)
            print(f"{sc.getpeername()} connected!")

    def broadcast(self, message, source):
        # send to all connected client accept the source client
        for connection in self.connections:
            if connection.sockname != source:
                connection.send(message)

        print ("send broadcast: ", message)

    def serverBroadcast(self, message):
        # send to all connected client
        for connection in self.connections:
            connection.send(message)
            
        print ("send server broadcast: ", message)

    def sendTo(self, message, destination):
        # send to specific client
        for connection in self.connections:
            if connection.sockname == destination:
                connection.send(message)
                
        print ("send message: ", message)

    def remove_connection(self, connection):
        self.connections.remove(connection)


class ServerSocket(threading.Thread):
    def __init__(self, sc, sockname, server):
        super().__init__()
        self.sc = sc
        self.sockname = sockname
        self.username = None
        self.server = server

    def run(self):
        while True:
            # Receive message
            message = self.receive()

            if message:
                # Get to know what response he want
                signal = message.split(';')[0]

                if signal == "[auth]":
                    username = message.split(';')[1].lower()

                    # Check if this username are already logged in
                    if username in [connection.username for connection in self.server.connections] or not username in usernames :
                        self.server.sendTo("[response];fail;[end]", self.sockname)
                        self.server.remove_connection(self)
                        self.sc.close()

                    # Log in
                    else:
                        self.username = username
                        self.server.sendTo("[response];ok;[end]", self.sockname)
                        self.server.broadcast("[message];Server;{} has joined the chat;[end]".format(self.username), self.sockname)

                elif signal == "[image]":
                    pass

                elif signal == "[message]":
                    self.server.broadcast(message, self.sockname)
                
            else:
                print(f"""{self.username} has closed the connection""")
                self.sc.close()
                self.server.remove_connection(self)
                return

    def send(self, message):
        self.sc.sendall(message.encode('utf-8'))

    def receive(self):
        message = ""
        while (True):
            try: message += self.sc.recv(1024).decode('utf-8')
            except: return None

            if message.__contains__("[end]"):
                print ("message receive: {}".format(message))
                return message


def console(server):
    while (True):
        ipt = input("")
        if ipt == "q":
            print("Closing all connections...")
            for connection in server.connections:
                connection.sc.close()

            print("Shutting down the server...")
            os._exit(0)

        if ipt.split(' ')[0] == "/ban" and ipt.split(' ')[1][0] == '1':
            ip = ipt.split(' ')[1]
            if ip in [connection.sockname[0] for connection in server.connections]:
                for connection in server.connections:
                    if connection.sockname[0] == ip:
                        server.broadcast("[message];Server: {} have been banned from the server;[end]".format(connection.username), connection.sockname)
                        connection.sc.close()
                        
            else:
                print("[ALERT!] IP unavailable!")

        elif ipt.split(' ')[0] == "/ban":
            username = ipt.split(' ')[1]
            if username in [connection.username for connection in server.connections]:
                for connection in server.connections:
                    if connection.username == username:
                        server.broadcast("[message];Server: {} have been banned from the server;[end]".format(connection.username), connection.sockname)
                        connection.sc.close()

            else:
                print("[ALERT!] username unvailable")

        if ipt.split(' ')[0] == "/list":
            print ("--------------------------------")
            print ("List user:")
            for i, connection in enumerate(server.connections):
                print("{}. {}\t{}".format(i, connection.username, connection.sockname[0]))
            
            print ("--------------------------------")

        if ipt.split(' ')[0] == "/clear_gdocs":
            server.data = []

            with open(DATA_PATH, "w") as f:
                f.write(json.dumps(server.data))

            print("gdocs cleared")
            server.serverBroadcast("[data];[];[end]")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chatroom Server")
    parser.add_argument('host', help='Interface the server lintens at')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060, help='TCP port(default 1060)')

    args = parser.parse_args()

    # Create and start server thread
    server = Server(args.host, args.p)
    server.start()

    console = threading.Thread(target=console, args=(server,))
    console.start()

