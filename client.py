import sys
import socket
import selectors
import json

from libclient.message import *
from libclient.messages import *

class Client:
    def __init__(self, address):
        self.address = address
        self.sel = selectors.DefaultSelector()
        self.messages = Messages()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start_connection(self):
        """Called when connecting to a server for the first time"""
        print("Beginning connection to", address)
        try:
            self.sock.connect(self.address)
        except Exception:
            print(f'Can\'t connect to server, connection refused')
            exit(1)
        try:
            self.message = Message(self.sock)
            self.listen()
        except Exception:
            self.server_closed()

    def listen(self):
        """Main listening loop"""
        while True:
            data_buffer = self.sock.recv(4)
            if data_buffer:
                length = struct.unpack('<i', data_buffer)
                data = self.sock.recv(length[0])
                print("Received data of length", length)
                message = self._json_decode(data)
                self.message.handle_listener(message)
            else:
                self.server_closed()

    def server_closed(self):
        """Closes the client when server connection is lost"""
        print(f'Connection to server lost, closing client')
        self.sock.close()
        exit(0)
                
    def _json_decode(self, json_bytes):
        """returns a decoded json object from encoding: utf-8."""
        json_msg = json.loads(json_bytes)
        return json_msg

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("Usage: client.py -i [host] -p [port]")
        sys.exit(1)
    host = sys.argv[2]
    port = int(sys.argv[4])
    address = (host, port)
    client = Client(address)
    try:
        client.start_connection()
    except KeyboardInterrupt:
        print("Gracefully exiting, keyboard interrupt")
    finally:
        client.sel.close()
