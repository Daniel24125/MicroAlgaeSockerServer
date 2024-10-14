import sys
import os
import socketio
from threading import Thread
from aiohttp import web

SEND_TIMES = 5


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from utils import env_handler, logger, utils
from .command_socket import CommandSocket

PORT = int(env_handler.load_env("NEXTJS_PORT"))

    
sio = socketio.AsyncServer(cors_allowed_origins='*', async_mode='aiohttp')
app = web.Application()
sio.attach(app)

subscriber = utils.SubscriberClass(sio)   
command_instance = CommandSocket(subscriber.notify_subscribers)


@sio.event
def connect(sid, environ, auth):
    logger.log("[NextJS Python Socket Server] Client connected with the id " + sid, severity="info")
    

@sio.event
def disconnect(sid):
    logger.log(f"The client with id {sid} has been disconnected")
    handle_client_disconnection(sid)
    
    
@sio.event
async def identification(sid, data):
    logger.log(f"[NextJS Python Socket Server] Parsing the following command: identification", "info")
    await identification(data, sid)

@sio.event
def test(sid, data):
    logger.log(f"[NextJS Python Socket Server] TEST " + data, "info")

def start_server():
    logger.log(f"[NextJS Python Socket Server] Server listenning on port {PORT}", severity="info")
    web.run_app(app, port=PORT)
       

def handle_client_disconnection(sid): 
    subscriber.unsubscribe(sid)



# Available commands
async def identification(data, sid, *argv):
    if data == "next": 
        logger.log("[NextJS Python Socket Server] NEXJS Client connected!", severity="info")
        subscriber.add_subscriber_to_list(sid)
        print(command_instance.get_spec_socket())
        # await initiate_command_socket()


# Utils
async def initiate_command_socket(): 
    if subscriber.get_num_subscribers() == 1:
        logger.log("[NextJS Python Socket Server] Establishing connection with Spectrometer Socket Server", severity="default")
        await command_instance.wait_for_commands()
      
def send_client_command(cmd, sid):
    logger.log("[NextJS Python Socket Server] Sending a command to the client", severity="default")
    print("Sending client a message", sid)
    sio.emit("test", cmd, to=sid)


   





    
# class NextSocketServer(utils.SocketServer): 
#     def __init__(self): 
#         asyncio.run(self.start_server())

#     async def start_server(self):
#         async with serve( self.client_connected, host="", port=PORT):
#             logger.log(f"[NextJS Python Socket Server] Server listenning on port {PORT}", severity="info")
#             self.subscriber = utils.SubscriberClass()
#             await asyncio.Future()
   

#     async def client_connected(self,client_socket):
#         logger.log("[NextJS Python Socket Server] Client connected!", severity="info")
#         try: 
#             t = threading.Thread(target=self.ping_client, args=(client_socket,))
#             t.start()
#             cmd = await client_socket.recv()
#             self.receive_cmd(cmd, client_socket)
#         except asyncio.CancelledError: 
#             logger.log("[NextJS Python Socket Server] ERROR " + str(err), severity="error")
#         # except Exception as err: 
#         except ConnectionClosed:
#             logger.log("[NextJS Python Socket Server] Client Disconnected", severity="error")
#         except Exception as err: 
#             logger.log(f"[NextJS Python Socket Server] The following error occured {err}", severity="error")

#     async def ping_client(self, client_socket): 
#         while True: 
#             await self.send_client_msg({"cmd": "ping"}, client_socket)

#     async def send_client_msg(self, msg, client_socket): 
#         await client_socket.send(bytes(json.dumps(msg), "utf-8"))

#     def parse_cmd(self, cmd, client_socket):
#         commands = {
#             "identification": self.identification,
#             "notify_subscribers": self.notify_subscribers
#         }
#         super().parse_cmd(cmd, client_socket, commands)

#     def handle_client_disconnection(self, client_socket): 
#         super().handle_client_disconnection(client_socket)
#         if self.subscriber.get_num_subscribers == 0: 
#             self.command_instance.disconnect()

#     # Available commands
#     def identification(self, data, client_socket, *argv):
#         if data == "next": 
#             logger.log("[NextJS Python Socket Server] NEXJS Client connected!", severity="info")
#             self.next_client_socket = client_socket
#             self.subscriber.add_subscriber_to_list(client_socket)
#             self.initiate_command_socket(client_socket)
            

#     def notify_subscribers(self): 
#         self.subscriber.notify_subscribers()

#     # Utils
#     def initiate_command_socket(self, client_socket): 
#         if self.subscriber.get_num_subscribers == 0:
#             t1 = threading.Thread(target= self.make_command_socket_connection, args=(client_socket,))
#             t1.start()

#     def make_command_socket_connection(self, client_socket): 
#         self.command_instance = CommandSocket(client_socket)
        