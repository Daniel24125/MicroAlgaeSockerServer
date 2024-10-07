import asyncio
from websockets.server import serve
import websockets
import sys
import os
import threading

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from utils import env_handler, logger, utils
from .command_socket import CommandSocket

PORT = env_handler.load_env("NEXTJS_PORT")

class NextSocketServer(utils.SocketServer): 
    def __init__(self): 
        asyncio.run(self.start_server())

    async def start_server(self):
        async with serve( self.client_connected, host="", port=PORT):
            logger.log(f"[NextJS Python Socket Server] Server listenning on port {PORT}", severity="info")
            self.subscriber = utils.SubscriberClass()
            await asyncio.Future()
   

    async def client_connected(self,client_socket):
        logger.log("[NextJS Python Socket Server] Client connected!", severity="info")
        async for cmd in client_socket:
            try: 
                self.receive_cmd(cmd, client_socket)
            except websockets.exceptions.ConnectionClosed:
                logger.log("[NextJS Python Socket Server] Client Disconnected", severity="error")
            except Exception as err: 
                logger.log(f"[NextJS Python Socket Server] The following error occured {err}", severity="error")

    def parse_cmd(self, cmd, client_socket):
        commands = {
            "identification": self.identification,
            "notify_subscribers": self.notify_subscribers
        }
        super().parse_cmd(cmd, client_socket, commands)

    def handle_client_disconnection(self, client_socket): 
        super().handle_client_disconnection(client_socket)
        if self.subscriber.get_num_subscribers == 0: 
            self.command_instance.disconnect()

    # Available commands
    def identification(self, data, client_socket, *argv):
        if data == "next": 
            logger.log("[NextJS Python Socket Server] NEXJS Client connected!", severity="info")
            self.next_client_socket = client_socket
            self.subscriber.add_subscriber_to_list(client_socket)
            self.initiate_command_socket(client_socket)

    def notify_subscribers(self): 
        self.subscriber.notify_subscribers()

    # Utils
    def initiate_command_socket(self, client_socket): 
        if self.subscriber.get_num_subscribers == 0:
            t1 = threading.Thread(target= self.make_command_socket_connection, args=(client_socket,))
            t1.start()

    def make_command_socket_connection(self, client_socket): 
        self.command_instance = CommandSocket(client_socket)
        


if __name__ == "__main__": 
    server = NextSocketServer()
    