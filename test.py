import asyncio
from websockets.server import serve

PORT = 9000

async def echo(websocket):
    print("client connected")
    async for message in websocket:
        print(message)
        # await websocket.send(message)


async def main():
    async with serve( echo, host="", port=PORT):
        print("Server listenning on port ", PORT)
        # connect_to_server()
        await asyncio.get_running_loop().create_future()  # run forever

# asyncio.run(main())

