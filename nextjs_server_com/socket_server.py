import sys
import os
import socketio
from aiohttp import web
import asyncio 


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from utils import env_handler, logger, utils

PORT = int(env_handler.load_env("NEXTJS_PORT"))

    
sio = socketio.AsyncServer(cors_allowed_origins='*', async_mode='aiohttp')
app = web.Application()
sio.attach(app)

subscriber = utils.SubscriberClass(sio)   
command_instance = None


@sio.event
def connect(sid, environ, auth):
    logger.log("Client connected with the id " + sid, context="NextJS Python Socket Server", severity="info")
    
@sio.event
def disconnect(sid):
    logger.log(f"The client with id {sid} has been disconnected",context="NextJS Python Socket Server")
    handle_client_disconnection(sid)
    
@sio.event
async def identification(sid, data):
    logger.log(f"Parsing the following command: identification",context="NextJS Python Socket Server", severity="info")
    asyncio.create_task(identification(data, sid))

@sio.event
async def start_experiment(sid, data):
    logger.log(f"Parsing the following command: start_experiment",context="NextJS Python Socket Server", severity="info")
    command_instance.send_command_to_spec_server({
        "cmd": "start_experiment", 
        "data": "hello"
    })

@sio.event
async def stop_experiment(sid, data):
    logger.log(f"Parsing the following command: identification",context="NextJS Python Socket Server", severity="info")
    command_instance.send_command_to_spec_server({
        "cmd": "stop_experiment", 
        "data": "hello"
    })

@sio.event
def test(sid, data):
    logger.log(f"TEST " + data,context="NextJS Python Socket Server", severity="info")

def start_server(command_inst):
    global command_instance
    command_instance = command_inst
    logger.log(f"Server listenning on port {PORT}",context="NextJS Python Socket Server", severity="info")
    web.run_app(app, port=PORT)
       
def handle_client_disconnection(sid): 
    subscriber.unsubscribe(sid)
  

# Available commands
async def identification(data, sid, *argv):
    if data == "next": 
        logger.log("NEXJS Client connected!",context="NextJS Python Socket Server", severity="info")
        subscriber.add_subscriber_to_list(sid)
        await subscriber.notify_user(sid)
        if subscriber.get_num_subscribers() == 1:
            command_instance.init_notifier(subscriber.notify_subscribers)

# Utils

def send_client_command(cmd, sid):
    logger.log("Sending a command to the client",context="NextJS Python Socket Server", severity="default")
    print("Sending client a message", sid)
    sio.emit("test", cmd, to=sid)

