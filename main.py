from cpp_server_com.socket_server import ServerSocket
from nextjs_server_com.socket_server import NextSocketServer
from utils.logger import log
import threading




if __name__ == "__main__": 
    try: 
        spec_server = ServerSocket()
        
        t1 = threading.Thread(target=spec_server.listen_for_connections)
        t1.start()
        next_server = NextSocketServer()

        
    except Exception as e: 
        log(e, "error")
