from cpp_server_com.socket_server import ServerSocket
import threading




if __name__ == "__main__": 
    try: 
        server = ServerSocket()
        t1 = threading.Thread(target=server.listen_for_connections)
        t1.start()
        print("HELLO")
        
    except Exception as e: 
        print(e)
