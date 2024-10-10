from cpp_server_com.socket_server import SpecServerSocket
from nextjs_server_com.socket_server import start_server
from utils.logger import log
import threading




if __name__ == "__main__": 
    try: 
        spec_server = SpecServerSocket()
        t1 = threading.Thread(target=spec_server.listen_for_connections)
        t1.start()

        # NextJS Scoket
        start_server()

        
    except Exception as e: 
        log(e, "error")
