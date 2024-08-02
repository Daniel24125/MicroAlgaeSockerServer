import asyncio
from websockets.server import serve
import json
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from utils import env_handler, logger
from .command_socket import CommandSocket

PORT = env_handler.load_env("NEXTJS_PORT")

class NextSocketServer: 
    def __init__(self): 
        asyncio.run(self.connect_server())

    async def connect_server(self):
        async with serve( self.client_connected, host="", port=PORT):
            logger.log(f"Server listenning on port {PORT}", severity="info")
            await asyncio.Future()
   
    async def client_connected(self,websocket):
        logger.log("Client connected!", severity="info")
        async for message in websocket:
            try: 
                self.receive_cmd(message, websocket)
            except Exception as err: 
                logger.log(f"The following error occured {err}", severity="error")


    def receive_cmd(self, data, client_socket):

        if not len(data): 
            self.handle_client_disconnection(client_socket)           
            # raise Exception("An error occured while trying to receive a command, probably due to client disconnection.")
        
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
        if data == "next": 
            logger.log("NEXJS Client connected!", severity="info")
            self.next_client_socket = client_socket
            self.command_instance = CommandSocket(client_socket)

        self.sockets_list.append(client_socket)

    def nir_status(self, _ , status): 
        logger.log("Updating spec status...", "info")
        if bool(self.spec): 
            self.spec.nir_status(status)

    def handle_client_disconnection(self, client_socket): 
        logger.log("The client has been disconnected")


if __name__ == "__main__": 
    server = NextSocketServer()
    