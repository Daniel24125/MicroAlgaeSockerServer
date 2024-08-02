
import sys
import os
import socket
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from utils import env_handler, logger

HOST = env_handler.load_env("CPP_HOST")
PORT = int(env_handler.load_env("CPP_PORT"))

class CommandSocket: 
    
    def __init__(self, next_client_socket): 
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                logger.log("Trying to connect to the server", severity="info")
                s.connect((HOST, PORT))
                self.socket = s
                self.next_client_socket = next_client_socket
                self.send_command({
                    "cmd": "identification",
                    "data": "next"
                })
                self.wait_for_commands()
            except: 
                logger.log("Spectrometer server not available!", severity="error")
    
    def wait_for_commands(self): 
        while True:
            data = self.socket.recv(1024)
            logger.log("Command received: " + data, severity="info")
            self.next_client_socket.send(data)
    
    def send_command(self, msg): 
        self.socket.send(bytes(json.dumps(msg), encoding="utf-8"))

if __name__ == "__main__": 
    cmd = CommandSocket()
