
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from cpp_server_com.HSSUSB2A import HSSUSB2A
import json
import time
import socket
import select
from utils import env_handler, logger, utils


HOST = env_handler.load_env("CPP_HOST") 
PORT = int(env_handler.load_env("CPP_PORT"))

class SpecServerSocket(utils.SocketServer): 
    device_socket = None
    
    def __init__(self, port=PORT): 
        super().__init__()
        self.init_socket(port)

    def init_socket(self, port): 
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sockets_list = [self.server_socket]
        self.server_socket.bind((HOST, port))
        self.server_socket.listen()
        logger.log(f"Server listenning on port {port}", context="Python Spec Socket", severity="info")

    def listen_for_connections(self): 
        while True: 
            read_socket, _ , exception_sockets = select.select(self.sockets_list, [], self.sockets_list)
            for notified_socket in read_socket: 
                try: 
                    if notified_socket == self.server_socket: 
                        client_socket, client_address = self.server_socket.accept()
                        logger.log(f"A client has connected with the following address: {client_address}",context="Python Spec Socket",severity="default")
                        self.handle_data_reception(client_socket)
                    else: 
                        self.handle_data_reception(notified_socket)

                except ConnectionResetError as e: 
                    self.handle_client_disconnection(notified_socket)
                except Exception as err: 
                    logger.log(f"An error occured: {str(err)}",context="Python Spec Socket",severity="error")   
            time.sleep(1)
    
    def handle_data_reception(self, client_socket):
        logger.log("Waiting for Commands", context="Python Spec Socket",severity="default")
        try: 
            data = client_socket.recv(1024) 
        except socket.timeout as e:
            err = e.args[0]
            if err != 'timed out':
                logger.log("Error while receiving data: " + str(e),context="Python Spec Socket", severity="error")
        except socket.error as e:
            self.handle_client_disconnection(client_socket)
        else: 
            if len(data) == 0: 
                   self.handle_client_disconnection(client_socket)
                   
            else: 
                self.receive_cmd(data, client_socket=client_socket)

    def parse_cmd(self, cmd, client_socket):
        commands = {
            "identification": self.identification,
            "device_status": self.device_status
        }
        super().parse_cmd(cmd, client_socket, commands)

    # ------------- Available spectrometer commands -----------------
    def identification(self, data, client_socket, *argv):
        if data == "nir": 
            self.nir_spec_init(client_socket)
        elif data == "next": 

            self.command_socket_init(client_socket)     
        else: 
            raise Exception("Unauthorized connection.")
        self.sockets_list.append(client_socket)

    def nir_spec_init(self, socket): 
        logger.log("Initializing the Spectrometer instance...",context="Python Spec Socket", severity="info")
        self.device_socket = socket
        self.spec = HSSUSB2A(socket)

    def command_socket_init(self, socket): 
        logger.log("Command Client connected",context="Python Spec Socket", severity="info")
        self.command_client_socket = socket
        self.experiment_data.register_command_socket(socket=socket)
            
    def device_status(self, data , socket): 
        logger.log("Updating spec status...",context="Python Spec Socket", severity="info")
        self.spec.device_status(socket)
        logger.log("Retrieving experimental data to NEXJS Server",context="Python Spec Socket", severity="warning")
        self.send_client_commands({"cmd": "notify_subscribers", "data": data})
    
    # ------------- Utils methods -----------------
    def handle_client_disconnection(self, client_socket): 
        super().handle_client_disconnection(client_socket)
        if client_socket == self.device_socket: 
            self.reset_socket()
        self.sockets_list.remove(client_socket)

    def reset_socket(self):
        self.device_socket = None
        self.spec.set_device_socket(None)
        self.experiment_data.update_experiment_data({
            "isDeviceConnected": False
        }, True)

    def send_client_commands(self, msg): 
        if hasattr(self, "command_client_socket"):
            
            self.command_client_socket.send(bytes(json.dumps(msg),encoding="utf-8"))
        else:
            logger.log("Nextjs client not available!", context="Python Spec Socket", severity="info")
    
    def send_spectrometer_command(self, msg): 
        if hasattr(self, "device_socket"):
            self.device_socket.send(bytes(json.dumps(msg),encoding="utf-8"))

if __name__ == "__main__": 
    server = SpecServerSocket()
    server.listen_for_connections()














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

# async def device_status(data, client_socket): 
#     spec_data = spec if bool(spec) else "Spectrometer not connected!"
#     await client_socket.send(spec_data)

# COMMANDS = {
#     "identification": identification,
#     "device_status": device_status
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