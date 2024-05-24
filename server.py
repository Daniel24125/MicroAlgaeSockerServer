import socket
import time 
import select
import json


HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 3000  # Port to listen on (non-privileged ports are > 1023)

class ServerSocker: 
    nir_socket = None
    is_nir_init = False


    def __init__(self, port=PORT): 
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sockets_list = [self.server_socket]
        self.server_socket.bind((HOST, port))
        self.server_socket.listen()
        print(f"Server listenning on {port}")

    def receive_cmd(self, client_socket, removeFromList=False):
        data = client_socket.recv(1024)
        
        if not len(data): 
            if removeFromList: 
                self.sockets_list.remove(client_socket)
            raise Exception("An error occured while trying to receive a command, probably due to client disconnection.")
                   
        cmd = json.loads(data)
        print(f"Command received: {cmd}")
        return cmd
    
    def init_nir(self, client_socket):
        self.nir_socket = client_socket
        print("Requesting NIR status information")
        send_data = bytes(json.dumps({
            "cmd": "nir_status"
        }), "utf-8")
        client_socket.send(send_data)


    def parse_cmd(self, cmd, client_socket):
        if not "cmd" in cmd: 
            raise Exception("Invalid JSON received")
        cmd_received = cmd["cmd"]
        print(f"Parsing the following command: {cmd_received}")
        if  cmd_received == "identification": 
            data = cmd["data"]
            if data == "nir": 
                self.init_nir(client_socket)
            elif data == "user":
                self.socket_list.append(client_socket)

        else:
            raise Exception("Command not recongnized")
         

    def listen_for_connections(self): 
        while True: 
            read_socket, _ , exception_sockets = select.select(self.sockets_list, [], self.sockets_list)
            print(read_socket)
            for notified_socket in read_socket: 
                if notified_socket == self.server_socket: 
                    client_socket, client_address = self.server_socket.accept()
                    print(f"A client has connected with the following address: {client_address}")

                    cmd = self.receive_cmd(client_socket)
                    self.parse_cmd(cmd, client_socket)
                else: 
                    cmd = self.receive_cmd(notified_socket, True)

            time.sleep(1)



if __name__ == "__main__": 
    try:
        server = ServerSocker()
        server.listen_for_connections()
    except Exception as e: 
        print(e)


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
