from utils.HSSUSB2A import HSSUSB2A
import socket
import time 
import select
import json


HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 8000  # Port to listen on (non-privileged ports are > 1023)

class ServerSocker: 
    spec = None
    
    def __init__(self, port=PORT): 
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sockets_list = [self.server_socket]
        self.server_socket.bind((HOST, port))
        self.server_socket.listen()
        print(f"Server listenning on {port}")

    def identification(self, data, client_socket, *argv):
        if data == "nir": 
            self.init_nir(client_socket)
        self.sockets_list.append(client_socket)

   

    def receive_cmd(self, client_socket):
        data = client_socket.recv(1024) 
        if not len(data): 
            if client_socket == self.nir_socket: 
                self.handle_client_disconnection(client_socket)           
            raise Exception("An error occured while trying to receive a command, probably due to client disconnection.")
                   
        print(f"Command received: {data}")
        cmd = json.loads(data)
        
        self.parse_cmd(cmd, client_socket)
    
    def init_nir(self, client_socket):
        self.spec = HSSUSB2A(client_socket)
        print("Requesting NIR status information")
        send_data = bytes(json.dumps({
            "cmd": "nir_status"
        }), "utf-8")
        self.spec.send_command(send_data)


    def parse_cmd(self, cmd, client_socket):
        commands = {
            "identification": self.identification,
            "nir_status": self.spec.nir_status
        }
        
        if not "cmd" in cmd: 
            raise Exception("Invalid JSON received")
        cmd_received = cmd["cmd"]
        data = cmd["data"]
        print(f"Parsing the following command: {cmd_received}")
        if cmd_received in commands: 
            commands[cmd_received](data, client_socket)
        else:
            print("Command not recognized")
         

    def listen_for_connections(self): 
        while True: 
                read_socket, _ , exception_sockets = select.select(self.sockets_list, [], self.sockets_list)
    
                for notified_socket in read_socket: 
                    try: 
                        if notified_socket == self.server_socket: 
                            client_socket, client_address = self.server_socket.accept()
                            print(f"A client has connected with the following address: {client_address}")
                            self.receive_cmd(client_socket)
                        else: 
                            print("Waiting for Commands...")
                            self.receive_cmd(notified_socket)

                    except ConnectionResetError as e: 
                        self.handle_client_disconnection(notified_socket)

                time.sleep(1)

    def handle_client_disconnection(self, client_socket): 
        print("The client has been disconnected")
        if client_socket == self.nir_socket: 
            self.spec.set_nir_socket(None)
        self.sockets_list.remove(client_socket)
