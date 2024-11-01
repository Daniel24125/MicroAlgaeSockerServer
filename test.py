# from twisted.internet import reactor, protocol
# import hashlib
# import base64
# import chardet
# from twisted.internet.protocol import connectionDone
# from twisted.python.failure import Failure
# import codecs


# class Echo(protocol.Protocol):
#     def __init__(self) -> None:
#         super().__init__()
#         self.handshake_buffer = b''

#     def connectionMade(self):
#         print('Got connection.')

#     def connectionLost(self, reason: Failure = ...) -> None:
#         print("Client disconnected: ", reason)
#         return super().connectionLost(reason)
            
#     def dataReceived(self, data):
#         """As soon as any data is received, write it back."""
#         self.handshake_buffer += data
#         if b"\r\n\r\n" in self.handshake_buffer:  # Check for end of HTTP header
#             # Complete handshake data received
#             print("Complete data")
#             self.handle_data_received(self.handshake_buffer)
#             self.handshake_buffer = b''  # Clear buffer for next handshake
#         else:
#             # More data expected, accumulate in the buffer
#             print("Accumulating handshake data...")
#             encoding = chardet.detect(data)['encoding']
#             print(data, encoding)
#         # self.handle_data_received(data)

#     def handle_data_received(self, data):
#         try:
#             encoding = chardet.detect(data)['encoding']
#             print("Encoding: ", encoding)
#             if encoding:
#                 # encoded_data = data.decode(encoding)
#                 encoded_data = codecs.decode(data, encoding)
#                 is_handhsake_data = encoded_data.find("GET") >= 0
#                 if is_handhsake_data: 
#                     print("Performing handshake")
#                     self.handle_handshake(encoded_data)
#                 else: 
#                     print("Data received: ", encoded_data)

                
#             else:
#                 # Handle unsupported encoding or invalid data
#                 print("Invalid data", data)
#                 return
#         except Exception as err: 
#             encoding = chardet.detect(data)['encoding']
#             print("Error on data: ", data, encoding)
            

#     def handle_handshake(self, data): 
#             request_headers = {}
#             for line in data.split('\r\n')[1:]:
#                 line = line.strip()
#                 if not line:
#                     break
#                 header, value = line.split(': ')
#                 request_headers[header.lower()] = value.strip()

#             sec_websocket_key = request_headers['sec-websocket-key']
#             key_concat = sec_websocket_key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
#             sha1_hash = hashlib.sha1(key_concat.encode('utf-8')).digest()
#             sec_websocket_accept = base64.b64encode(sha1_hash).decode('utf-8')

#             response = f"HTTP/1.1 101 Switching Protocols\r\n" \
#                     f"Upgrade: websocket\r\n" \
#                     f"Connection: Upgrade\r\n" \
#                     f"Sec-WebSocket-Accept: {sec_websocket_accept}\r\n" \
#                     f"\r\n"
#             self.transport.write(response.encode('utf-8'))




# def main():
#     factory = protocol.Factory.forProtocol(Echo)
#     reactor.listenTCP(8000, factory)
#     print("Listening on port 8000")
#     reactor.run()

import asyncio
import websockets

async def handle_websocket(websocket, path):
    print("Connection made!", path)
    try:
        async for message in websocket:
            print(f"Received WebSocket message: {message}")
            await websocket.send(f"Echo: {message}")
    except websockets.exceptions.ConnectionClosed:
        print("WebSocket connection closed")

async def handle_tcp(reader, writer):
    print("Connection made!")

    while True:
        data = await reader.read(100)
        if not data:
            break
        message = data.decode()
        print(f"Received TCP message: {message}")
        writer.write(f"Echo: {message}".encode())
        await writer.drain()
    writer.close()

async def main():
    nextjs_port = 8765
    nir_port = 8766

    websocket_server = await websockets.serve(handle_websocket, "localhost", nextjs_port)
    print("NEXTJS Server listenning on port " + str(nextjs_port))
    tcp_server = await asyncio.start_server(handle_tcp, "localhost", nir_port)
    print("NIR Server listenning on port " + str(nir_port))
    
    await asyncio.gather(websocket_server.wait_closed(), tcp_server.serve_forever())

asyncio.run(main())