from cpp_server_com.socket_server import SpecServerSocket
from utils.logger import log




if __name__ == "__main__": 
    try: 
        spec_server = SpecServerSocket()
        spec_server.listen_for_connections()
 

        
    except Exception as e: 
        log(e, "Error on Spec socket")
