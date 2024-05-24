import socket
import time 
import select
import json


HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 3000  # Port to listen on (non-privileged ports are > 1023)

class ServerSocker: 
    nir_socket = None
    is_nir_init = False


    def __init__(self, port=PORT): 
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sockets_list = [self.server_socket]
        self.server_socket.bind((HOST, port))
        self.server_socket.listen()
        print(f"Server listenning on {port}")

    def handle_client_disconnection(self, client_socket): 
        print("The client has been disconnected")
        if client_socket == self.nir_socket: 
            self.nir_socket = None
        self.sockets_list.remove(client_socket)

    def receive_cmd(self, client_socket):
        data = client_socket.recv(1024) 
        if not len(data): 
            if client_socket == self.nir_socket: 
                self.handle_client_disconnection(client_socket)           
            raise Exception("An error occured while trying to receive a command, probably due to client disconnection.")
                   
        print(f"Command received: {data}")
        cmd = json.loads(data)
        return cmd
    
    def init_nir(self, client_socket):
        self.nir_socket = client_socket
        print("Requesting NIR status information")
        send_data = bytes(json.dumps({
            "cmd": "nir_status"
        }), "utf-8")
        client_socket.send(send_data)


    def parse_cmd(self, cmd, client_socket):
        if not "cmd" in cmd: 
            raise Exception("Invalid JSON received")
        cmd_received = cmd["cmd"]
        data = cmd["data"]
        print(f"Parsing the following command: {cmd_received}")
        if  cmd_received == "identification": 
            if data == "nir": 
                self.init_nir(client_socket)
            self.sockets_list.append(client_socket)
        elif cmd_received == "nir_status":
            print("NIR Status received")
            self.is_nir_init = bool(data)
        else:
            print("Command not recongnized")
         

    def listen_for_connections(self): 
        while True: 
            read_socket, _ , exception_sockets = select.select(self.sockets_list, [], self.sockets_list)
            print("Exception sockets: ")
            print(exception_sockets)
            for notified_socket in read_socket: 
                if notified_socket == self.server_socket: 
                    client_socket, client_address = self.server_socket.accept()
                    print(f"A client has connected with the following address: {client_address}")
                    cmd = self.receive_cmd(client_socket)
                    self.parse_cmd(cmd, client_socket)
                else: 
                    print("Waiting for Commands...")
                    cmd = self.receive_cmd(notified_socket)
                    self.parse_cmd(cmd, notified_socket)


            time.sleep(1)

