import asyncio
from websockets.server import serve

import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from utils.env_handler import load_env



PORT = load_env("PORT")


async def echo(websocket):
    print("Client connected!")
    async for message in websocket:
        print(message)

async def main():
    async with serve( echo, host="", port=PORT):
        print("Server listenning on port ", PORT)
        await asyncio.get_running_loop().create_future()  # run forever


if __name__ == "__main__": 
    asyncio.run(main())