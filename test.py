import asyncio
from websockets.server import serve
from websockets.sync.client import connect
import socket

PORT = 8001

async def echo(websocket):
    print("client connected")
    async for message in websocket:
        print(message)
        # await websocket.send(message)

# def connect_to_server(): 
#         HOST = '127.0.0.1'    # The remote host
#         PORT = 8000              # The same port as used by the server
#         with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#             s.connect((HOST, PORT))
#             s.sendall(b'Hello, world')
#             data = s.recv(1024)
#         print('Received', repr(data))

async def main():
    async with serve( echo, host="", port=PORT):
        print("Server listenning on port ", PORT)
        # connect_to_server()
        await asyncio.get_running_loop().create_future()  # run forever

# asyncio.run(main())

