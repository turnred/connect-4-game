import sys
import socket
import selectors
from libserver.message import *
from libserver.messages import *

class Server:
    def __init__(self, port: int) -> None:
        self.port = port
        self.sel = selectors.DefaultSelector()
        self.connected = {}
        self.message = Message(self.sel, self.connected)
        self.messages = Messages()

    def build_server(self):
        """Establishes a listening socket"""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.sock.bind(('', self.port))
        except Exception:
            print("Fatal Error: Cannot bind port given")
        self.sock.listen()
        print("Server listening on port", port)
        
    def build_connection(self, sock):
        """Called when a client connects for the first time"""
        connection, address = sock.accept()
        print("Recieved connection from client", address)
        if len(self.connected) >= 2:
            print("Server can only support 2 clients, rejecting client...")
            connection.sendall(self.messages.msg_refuseconn("playerlimit"))
            connection.shutdown()
            return
        self.connected[connection] = address
        self.message.create_user(address)
        self.sel.register(connection, selectors.EVENT_READ | selectors.EVENT_WRITE)
        connection.sendall(self.messages.msg_acceptconn())

    def close_connection(self, sock):
        """Closes the client's lingering sockets when the server connection is dropped"""
        address = self.connected.pop(sock)
        self.sel.unregister(sock)
        print(f'Connection lost to client at{address}, removing client.')

    def listen(self):
        """Main listening loop"""
        self.build_server()
        while True:
            for key, _ in self.sel.select():
                sock = key.fileobj
                if sock is self.sock:
                    self.build_connection(sock)
                else:
                    if key.events & selectors.EVENT_READ:
                        self.message.read(sock)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: server.py -p [port]")
        sys.exit(1)
    port = int(sys.argv[2])
    server = Server(port)
    try:
        server.listen() 
    except KeyboardInterrupt:
        print("Gracefully exiting, keyboard interrupt")
    finally:
        server.sel.close()
