from cpp_server_com.socket_server import SpecServerSocket
from utils.logger import log




if __name__ == "__main__": 
    spec_server = SpecServerSocket()
    try: 
        spec_server.init_socket()
        spec_server.listen_for_connections()

    except KeyboardInterrupt: 
        print("INTERRUPT")    
    except Exception as e: 
        log(e, "Error on Spec socket")
