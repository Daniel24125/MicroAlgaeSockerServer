from twisted.internet import reactor, protocol
import hashlib
import base64
import chardet
from twisted.internet.protocol import connectionDone
from twisted.python.failure import Failure



class Echo(protocol.Protocol):
    def __init__(self) -> None:
        super().__init__()

    def handle_handshake(self, data): 
        request_headers = {}
        for line in data.split('\r\n')[1:]:
            line = line.strip()
            if not line:
                break
            header, value = line.split(': ')
            request_headers[header.lower()] = value.strip()

        sec_websocket_key = request_headers['sec-websocket-key']
        key_concat = sec_websocket_key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
        sha1_hash = hashlib.sha1(key_concat.encode('utf-8')).digest()
        sec_websocket_accept = base64.b64encode(sha1_hash).decode('utf-8')

        response = f"HTTP/1.1 101 Switching Protocols\r\n" \
                f"Upgrade: websocket\r\n" \
                f"Connection: Upgrade\r\n" \
                f"Sec-WebSocket-Accept: {sec_websocket_accept}\r\n" \
                f"\r\n"
        self.transport.write(response.encode('utf-8'))

    def handle_data_received(self, data):
        try:
            encoding = chardet.detect(data)['encoding']
            if encoding:
                encoded_data = data.decode(encoding)
                is_handhsake_data = encoded_data.find("GET") >= 0
                if is_handhsake_data: 
                    self.handle_handshake(encoded_data)
                else: 
                    print("Data received: ", data)

                
            else:
                # Handle unsupported encoding or invalid data
                print("Invalid data")
                return
        except Exception as err: 
            encoding = chardet.detect(data)['encoding']
            print("Error on data: ", data, encoding)
            
            
    def dataReceived(self, data):
        """As soon as any data is received, write it back."""
        self.handle_data_received(data)

    def connectionMade(self):
        print('Got connection.')

    def connectionLost(self, reason: Failure = ...) -> None:
        print("Client disconnected: ", reason)
        return super().connectionLost(reason)

def main():
    factory = protocol.Factory.forProtocol(Echo)
    reactor.listenTCP(8000, factory)
    print("Listening on port 8000")
    reactor.run()

if __name__ == '__main__':
    main()