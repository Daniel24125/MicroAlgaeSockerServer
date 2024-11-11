import websockets
import asyncio
from resources import env_handler, logger, utils
HOST = env_handler.load_env("CPP_HOST")
CPP_PORT = int(env_handler.load_env("CPP_PORT"))
NEXTJS_PORT = int(env_handler.load_env("NEXTJS_PORT"))

async def handle_next_connection(websocket, path):
    print("Connection made!", path)
    try:
        async for message in websocket:
            logger.log(f"Received WebSocket message: {message}", "MAIN - Nextjs Connection", "info")
            await websocket.send(f"Echo: {message}")
    except websockets.exceptions.ConnectionClosed:
        logger.log("A client was disconnected.", "MAIN - Nextjs Connection", "info")



async def handle_device_connection(reader, writer):
    print("Connection made!")
    logger.log("A device connection was made", "MAIN - NIR Connection", "info")

    while True:
        data = await reader.read(100)
        if not data:
            break
        message = data.decode()
        logger.log(f"Received TCP message: {message}", "MAIN - NIR Connection", "info")

        writer.write(f"Echo: {message}".encode())
        await writer.drain()
    writer.close()


async def main():

    websocket_server = await websockets.serve(handle_next_connection, HOST, NEXTJS_PORT)
    logger.log("NEXTJS Server listenning on port " + str(NEXTJS_PORT), "MAIN", "info")
    tcp_server = await asyncio.start_server(handle_device_connection, HOST, CPP_PORT)
    logger.log("NIR Server listenning on port " + str(CPP_PORT), "MAIN", "info")    
    await asyncio.gather(websocket_server.wait_closed(), tcp_server.serve_forever())


if __name__ == "__main__": 
    asyncio.run(main())