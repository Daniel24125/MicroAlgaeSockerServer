from nextjs_server_com.socket_server import start_server
from utils.logger import log
from threading import Thread
from nextjs_server_com.command_socket import CommandSocket
import asyncio 


if __name__ == "__main__": 
    try: 
        command_instance = CommandSocket()
        t = Thread(target=start_server, args=(command_instance,))
        t.start()
        t1 = Thread(target=asyncio.run, args=(command_instance.wait_for_commands(),))
        t1.start()
        t.join()        
    except Exception as e: 
        log(e, "Error on NextJS socket")
