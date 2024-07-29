from utils.HSSUSB2A import HSSUSB2A
import time 
import select
import json
import asyncio
from websockets.server import serve

HOST = ""  # Standard loopback interface address (localhost)
PORT = 8000  # Port to listen on (non-privileged ports are > 1023)
CONNECTIONS = set()
spec = None

def identification(data, client_socket, *argv):
    if data == "nir": 
        init_nir(client_socket)
    CONNECTIONS.add(client_socket)

async def nir_status(data, client_socket): 
    spec_data = spec if bool(spec) else "Spectrometer not connected!"
    await client_socket.send(spec_data)

COMMANDS = {
    "identification": identification,
    "nir_status": nir_status
}



async def client_connection_handler(websocket):
    print("Client Connected")
    async for message in websocket:
        try: 
            rvc_data = json.loads(message)
            await parse_cmd(rvc_data, websocket)
        except ValueError as e: 
            print("Error while processing the JSON data")
        # await websocket.send(message)

async def main():
    async with serve(client_connection_handler, host="", port=PORT):
        print("Server listenning on port ", PORT)

        await asyncio.get_running_loop().create_future()  # run forever

async def parse_cmd(cmd, client_socket):
    if not "cmd" in cmd: 
        raise Exception("Invalid JSON received")
    cmd_received = cmd["cmd"]
    data = cmd["data"]
    print(f"Parsing the following command: {cmd_received}")
    if cmd_received in COMMANDS:
        print(COMMANDS) 
        await COMMANDS[cmd_received](data, client_socket)
    else:
        print("Command not recognized")


def init_nir(client_socket):
    spec = HSSUSB2A(client_socket)
    print("Requesting NIR status information")
    send_data = bytes(json.dumps({
        "cmd": "nir_status"
    }), "utf-8")
    spec.send_command(send_data)

def handle_client_disconnection(client_socket): 
    print("The client has been disconnected")
    # if client_socket == self.nir_socket: 
    #     self.spec.set_nir_socket(None)
    CONNECTIONS.remove(client_socket)

class ServerSocker: 
    spec = None
    CONNECTIONS = set()
    # def __init__(self): 

        # self.sockets_list = [self.server_socket]
        # self.server_socket.bind((HOST, port))
        # self.server_socket.listen()
        # print(f"Server listenning on {port}")

    async def echo(self, websocket):
        async for message in websocket:
            print(message)
    
    async def listen(self): 
        self.server_socket = await serve( self.echo, host="", port=PORT)
        print("Server listenning on port ", PORT)


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
        try: 
            cmd = json.loads(data)
            self.parse_cmd(cmd, client_socket)
        except ValueError as e: 
            print("Error loading the json file. This probably occurs due to the first connection by the web client", e)
    
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
         

    async def listen_for_connections(self): 
        await asyncio.get_running_loop().create_future()

    def handle_client_disconnection(self, client_socket): 
        print("The client has been disconnected")
        if client_socket == self.nir_socket: 
            self.spec.set_nir_socket(None)
        self.sockets_list.remove(client_socket)
