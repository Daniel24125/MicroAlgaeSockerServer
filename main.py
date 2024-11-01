import websockets
import asyncio
from resources import ClientConnections, env_handler, logger, utils, experiment

## Variable Initialization
HOST = env_handler.load_env("CPP_HOST")
CPP_PORT = int(env_handler.load_env("CPP_PORT"))
NEXTJS_PORT = int(env_handler.load_env("NEXTJS_PORT"))
subscriber = utils.SubscriberClass()   
experiment_manager = experiment.Experiment()

async def handle_websocket(websocket, path):
    """
        fn: handle_websocket
        It handles the connections of the NextJS clients
        args: websocket, path
    """
    try:
        next_client = ClientConnections.NextJSClientConnection(websocket)
        next_client.init_experiment_manager(experiment_manager)
        await next_client.init_subscriber(subscriber)
        await next_client.listen_for_commands()
    
    except websockets.exceptions.ConnectionClosed:
        print("WebSocket connection closed")
        next_client.handle_disconnection()

    except Exception as err: 
        logger.log("An error occured in a NextJS connection: " + str(err), "Main", "error")
    


async def handle_tcp(reader, writer):
    print("Connection made!")

    while True:
        data = await reader.read(1024)
        if not data:
            break
        message = data.decode()
        print(f"Received TCP message: {message}")
        writer.write(f"Echo: {message}".encode())
        await writer.drain()
    writer.close()


async def main():
    websocket_server = await websockets.serve(handle_websocket, HOST, NEXTJS_PORT)
    logger.log("NEXTJS Server listenning on port " + str(NEXTJS_PORT), "Main", "info")
    tcp_server = await asyncio.start_server(handle_tcp, HOST, CPP_PORT)
    logger.log("NIR Server listenning on port " + str(CPP_PORT), "Main", "info")
    
    await asyncio.gather(websocket_server.wait_closed(), tcp_server.serve_forever())


if __name__ == "__main__": 
    try:
        asyncio.run(main())
    except Exception as err: 
        logger.log("An error occured: " + str(err), "Main", "error")