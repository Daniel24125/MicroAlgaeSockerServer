
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from utils.env_handler import load_env
import socket

HOST = load_env("CPP_HOST")
PORT = int(load_env("CPP_PORT"))

class CommandSocket: 
    def __init__(self): 
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(b'Hello, world')
            data = s.recv(1024)
            print(data)


if __name__ == "__main__": 
    cmd = CommandSocket()