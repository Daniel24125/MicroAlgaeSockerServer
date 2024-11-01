import websockets
import asyncio
from resources import env_handler, logger, utils
HOST = env_handler.load_env("CPP_HOST")
CPP_PORT = int(env_handler.load_env("CPP_PORT"))
NEXTJS_PORT = int(env_handler.load_env("NEXTJS_PORT"))

async def handle_websocket(websocket, path):
    print("Connection made!", path)
    try:
        async for message in websocket:
            print(f"Received WebSocket message: {message}")
            await websocket.send(f"Echo: {message}")
    except websockets.exceptions.ConnectionClosed:
        print("WebSocket connection closed")



async def handle_tcp(reader, writer):
    print("Connection made!")

    while True:
        data = await reader.read(100)
        if not data:
            break
        message = data.decode()
        print(f"Received TCP message: {message}")
        writer.write(f"Echo: {message}".encode())
        await writer.drain()
    writer.close()


async def main():

    websocket_server = await websockets.serve(handle_websocket, HOST, NEXTJS_PORT)
    print("NEXTJS Server listenning on port " + str(NEXTJS_PORT))
    tcp_server = await asyncio.start_server(handle_tcp, HOST, CPP_PORT)
    print("NIR Server listenning on port " + str(CPP_PORT))
    
    await asyncio.gather(websocket_server.wait_closed(), tcp_server.serve_forever())


if __name__ == "__main__": 
    asyncio.run(main())