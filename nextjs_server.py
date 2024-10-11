from nextjs_server_com.socket_server import start_server
from utils.logger import log

if __name__ == "__main__": 
    try: 
        start_server()

        
    except Exception as e: 
        log(e, "Error on NextJS socket")
