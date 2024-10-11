import sys
import os
import threading
import socketio


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from utils import env_handler, logger, utils
from .command_socket import CommandSocket

PORT = int(env_handler.load_env("NEXTJS_PORT"))
import eventlet


    
sio = socketio.Server(cors_allowed_origins='*')
subscriber = utils.SubscriberClass(sio)   
command_instance = None

@sio.event
def connect(sid, environ, auth):
    logger.log("[NextJS Python Socket Server] Client connected with the id " + sid, severity="info")

@sio.event
def disconnect(sid):
    logger.log(f"The client with id {sid} has been disconnected")
    handle_client_disconnection(sid)
    
    


@sio.event
def identification(sid, data):
    logger.log(f"[NextJS Python Socket Server] Parsing the following command: identification", "info")
    identification(data, sid)

@sio.event
def notify_subscribers():
    logger.log(f"[NextJS Python Socket Server] Parsing the following command: notify_subscribers", "info")
    notify_subscribers()

def start_server():
    app = socketio.WSGIApp(sio)
    logger.log(f"[NextJS Python Socket Server] Server listenning on port {PORT}", severity="info")
    eventlet.wsgi.server(eventlet.listen(('', PORT)), app)


def handle_client_disconnection(sid): 
    subscriber.unsubscribe(sid)
    if subscriber.get_num_subscribers() == 0 and command_instance: 
        command_instance.disconnect()


# Available commands
def identification(data, sid, *argv):

    if data == "next": 
        logger.log("[NextJS Python Socket Server] NEXJS Client connected!", severity="info")
        initiate_command_socket()
        subscriber.add_subscriber_to_list(sid)
        
def notify_subscribers(): 
    subscriber.notify_subscribers()

# Utils
def initiate_command_socket(): 
    # logger.log("[NextJS Python Socket Server] Num subs: " + str(), severity="default")

    if subscriber.get_num_subscribers() == 0:
        logger.log("[NextJS Python Socket Server] Establishing connection with Spectrometer Socket Server", severity="default")
        t1 = threading.Thread(target= make_command_socket_connection)
        t1.start()

def make_command_socket_connection(): 
    global command_instance
    command_instance = CommandSocket(sio)
        
if __name__ == "__main__": 
    # server = NextSocketServer()
    sio = socketio.Server(cors_allowed_origins='*')
    app = socketio.WSGIApp(sio)

    @sio.event
    def connect(sid, environ, auth):
        print('connect ', sid)

    @sio.event
    def disconnect(sid):
        print('disconnect ', sid)


    eventlet.wsgi.server(eventlet.listen(('', PORT)), app)







    
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
        