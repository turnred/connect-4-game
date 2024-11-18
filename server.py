import sys
import socket
import selectors
import types
from libserver.message import *

sel = selectors.DefaultSelector()
MAX_CONNECTIONS = 2
num_connected = 0

def build_server(host, port):
    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        lsock.bind((host, port))
    except Exception:
        print("server.py: Fatal Exception: Port Can't Be Bound")
    lsock.listen()
    lsock.setblocking(False)
    print("server.py: Server started on ", (host, port))
    sel.register(lsock, selectors.EVENT_READ, data=None)
    
def build_connection(sock):
    connection, address = sock.accept()
    print("server.py: Recieved connection from client", connection, address)
    if num_connected >= 2:
        print("server.py: Server can only support 2 clients, rejecting client...")
        connection.sendall(messages.conn_close())
        connection.close()
        return
    num_connected += 1
    connection.setblocking(False)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(connection, events, data=Message(sel, connection, address))

def get_num_connections():
    return num_connected

if len(sys.argv) != 3:
    print("Usage: server.py -p [PORT]")
    sys.exit(1)
host = '0.0.0.0'
port = int(sys.argv[2])
build_server(host, port)
try:
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                build_connection(key.fileobj)
            else:
                try:
                    key.data.process_events(mask)
                except Exception:
                    print("server.py: Error handling connection, assuming client has disconnected.")
                    key.data.close()
                    
except KeyboardInterrupt:
    print("Gracefully exiting, keyboard interrupt")
finally:
    sel.close()
