from utils.HSSUSB2A import HSSUSB2A
import json
import time
import socket
import asyncio
import select
from websockets.server import serve

# HOST = ""  # Standard loopback interface address (localhost)
# PORT = 8000  # Port to listen on (non-privileged ports are > 1023)
# CONNECTIONS = set()
# spec = None

# def identification(data, client_socket, *argv):
#     if data == "nir": 
#         print("NIR Socket Client detected!")
#         spec = HSSUSB2A(client_socket)
#     else:
#         CONNECTIONS.add(client_socket)

# async def nir_status(data, client_socket): 
#     spec_data = spec if bool(spec) else "Spectrometer not connected!"
#     await client_socket.send(spec_data)

# COMMANDS = {
#     "identification": identification,
#     "nir_status": nir_status
# }

# async def client_connection_handler(websocket):
#     print("Client Connected")
#     async for message in websocket:
#         try: 
#             rvc_data = json.loads(message)
#             await parse_cmd(rvc_data, websocket)
#         except ValueError as e: 
#             print("Error while processing the JSON data")
#         # await websocket.send(message)

# async def main():
#     async with serve(client_connection_handler, host="", port=PORT):
#         print("Server listenning on port", PORT)
#         await asyncio.get_running_loop().create_future()  # run forever

# async def parse_cmd(cmd, client_socket):
#     if not "cmd" in cmd: 
#         raise Exception("Invalid JSON received")
#     cmd_received = cmd["cmd"]
#     data = cmd["data"]
#     print(f"Parsing the following command: {cmd_received}")
#     if cmd_received in COMMANDS:
#         await COMMANDS[cmd_received](data, client_socket)
#     else:
#         print("Command not recognized")

# def handle_client_disconnection(client_socket): 
#     print("The client has been disconnected")
#     CONNECTIONS.remove(client_socket)
HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 8000  # Port to listen on (non-privileged ports are > 1023)

class ServerSocket: 
    spec = None
    
    def __init__(self, port=PORT): 
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sockets_list = [self.server_socket]
        self.server_socket.bind((HOST, port))
        self.server_socket.listen()
        print(f"Server listenning on {port}")

    def identification(self, data, client_socket, *argv):
        if data == "nir": 
            self.spec = HSSUSB2A(client_socket)
        self.sockets_list.append(client_socket)

    def receive_cmd(self, client_socket):
        data = client_socket.recv(1024) 
        if not len(data): 
            if hasattr(self, "nir_socket") and client_socket == self.nir_socket: 
                self.handle_client_disconnection(client_socket)           
            raise Exception("An error occured while trying to receive a command, probably due to client disconnection.")

        if data.find(b"GET") > -1: 
            self.response_to_user_connection(client_socket, data)
            return
        
        print(f"Command received: {data}")
        try: 
            cmd = json.loads(data)
            self.parse_cmd(cmd, client_socket)
        except ValueError as e: 
            print("Error loading the json file. This probably occurs due to the first connection by the web client", e)
            client_socket.send(b"Wrong JSON format")

    def response_to_user_connection(self, client_socket, request): 
        print("Connection from Browser client!")
        response_body = [
            '<html><body><h1>Hello, world!</h1></body/></html/>',
        ]
        response_headers = {
            'Content-Type': 'text/html; encoding=utf8',

       }
        response_body_raw = ''.join(response_body)

  
        response_proto = 'HTTP/1.1'
        response_status = '200'
        response_status_text = 'OK' # this can be random
        client_socket.send(bytes('%s %s %s' % (response_proto, response_status, \
                                                        response_status_text), encoding="utf-8"))
        client_socket.send(bytes(json.dumps(response_headers), encoding="utf-8"))
        client_socket.send(b'\n') # to separate headers from body
        client_socket.send(bytes(response_body_raw, encoding="utf-8"))

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
