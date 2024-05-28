from utils.socket_client import ServerSocker



if __name__ == "__main__": 
    server = ServerSocker()
    server.listen_for_connections()



    # server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # server_socket.bind((HOST, PORT))
    # server_socket.listen()
    # print(f"Server listenning on {PORT}")
    # client_socket, addr = server_socket.accept()
    # print(f"Client connected by {addr}")
    # client_socket.send(b"Welcome to the python server socket")
    # data = client_socket.recv(1024)
    # cmd = json.loads(data)

    # print(cmd["cmd"])
    # while True:
    #     read_socket, _ , exception_sockets = select.select()
        # with client_socket:
            # print(f"Client connected by {addr}")
            # client_socket.send(b"Welcome to the python server socket")
            # try:
            #     data = client_socket.recv(1024)
            #     if not data:
            #         break
            #     print(data)
            #     # client_socket.sendall(data)
            # except Exception as e:
            #     print("Client disconnected with the following error", repr(e))
            #     break
