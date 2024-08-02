from cpp_server_com.HSSUSB2A import HSSUSB2A
import json
import time
import socket
import select
from utils import env_handler, json_handler, logger


HOST = env_handler.load_env("CPP_HOST") 
PORT = int(env_handler.load_env("CPP_PORT"))

class ServerSocket: 
    spec = None
    
    def __init__(self, port=PORT): 
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sockets_list = [self.server_socket]
        self.server_socket.bind((HOST, port))
        self.server_socket.listen()
        logger.log(f"Server listenning on {port}", "info")
        self.experiment_data = json_handler.JSON_Handler()

    def listen_for_connections(self): 
        while True: 
            read_socket, _ , exception_sockets = select.select(self.sockets_list, [], self.sockets_list)
            for notified_socket in read_socket: 
                try: 
                    if notified_socket == self.server_socket: 
                        client_socket, client_address = self.server_socket.accept()
                        logger.log(f"A client has connected with the following address: {client_address}", "default")
                        self.receive_cmd(client_socket)
                    else: 
                        logger.log("Waiting for Commands...", "default")
                        self.receive_cmd(notified_socket)

                except ConnectionResetError as e: 
                    self.handle_client_disconnection(notified_socket)
                    
            time.sleep(1)

    def receive_cmd(self, client_socket):
        data = client_socket.recv(1024) 
        if not len(data): 
            if hasattr(self, "nir_socket") and client_socket == self.nir_socket: 
                self.handle_client_disconnection(client_socket)           
            raise Exception("An error occured while trying to receive a command, probably due to client disconnection.")
        
        logger.log(f"Command received: {data}", "info")
        try: 
            cmd = json.loads(data)
            self.parse_cmd(cmd, client_socket)
        except ValueError as e: 
            logger.log("Error loading the json file. This probably occurs due to the first connection by the web client" + e,"error")

    def parse_cmd(self, cmd, client_socket):
        commands = {
            "identification": self.identification,
            "nir_status": self.nir_status 
        }
        
        if not "cmd" in cmd: 
            raise Exception("Invalid JSON received")
        
        cmd_received = cmd["cmd"]
        data = cmd["data"]
        logger.log(f"Parsing the following command: {cmd_received}", "info")
        if cmd_received in commands: 
            commands[cmd_received](data, client_socket)
        else:
            logger.log("Command not recognized", "warning")
           
    # Available spectrometer commands
    def identification(self, data, client_socket, *argv):
        if data == "nir": 
            logger.log("Initializing the Spectrometer instance...", "info")
            self.nir_socket = client_socket
            self.spec = HSSUSB2A(client_socket)
        self.sockets_list.append(client_socket)

    def nir_status(self, client_socket, status): 
        logger.log("Updating spec status...", "info")
        if bool(self.spec): 
            self.spec.nir_status(status)

    def handle_client_disconnection(self, client_socket): 
        logger.log("The client has been disconnected")
        if client_socket == self.nir_socket: 
            self.nir_socket = None
            self.spec.set_nir_socket(None)
            self.experiment_data.update_experiment_data({
                "isDeviceConnected": False
            }, True)
        self.sockets_list.remove(client_socket)
















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


# def response_to_user_connection(self, client_socket, request): 
#         print("Connection from Browser client!")
#         response_body = [
#             '<html><body><h1>Hello, world!</h1></body/></html/>',
#         ]
#         response_headers = {
#             'Content-Type': 'text/html; encoding=utf8',

#        }
#         response_body_raw = ''.join(response_body)


#         response_proto = 'HTTP/1.1'
#         response_status = '200'
#         response_status_text = 'OK' # this can be random
#         client_socket.send(bytes('%s %s %s' % (response_proto, response_status, \
#                                                         response_status_text), encoding="utf-8"))
#         client_socket.send(bytes(json.dumps(response_headers), encoding="utf-8"))
#         client_socket.send(b'\n') # to separate headers from body
#         client_socket.send(bytes(response_body_raw, encoding="utf-8"))