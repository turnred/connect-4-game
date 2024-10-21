import sys
import socket
import selectors
import types

SEL = selectors.DefaultSelector()

def accept_connection(sock):
    connection, address = sock.accept()
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    SEL.register(connection, events, data=data)

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            data.outb += recv_data
        else:
            sel.unregister(sock)
            sock.close()
            print(data.addr, " connection closed")
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            sent = sock.send(data.outb)
            data.outb = data.outb[sent:]
            print("Echoed ", repr(data.outb), "to ", data.addr)

host = '0.0.0.0'
port = 35565
MAX_CONNECTIONS = 2

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)
print("Server started on ", (host, port))

try:
    while True:
        events = SEL.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                accept_connection(key.fileobj)
            else:
                service_connection(key, mask)
except KeyboardInterrupt:
    print("Gracefully exiting, keyboard interrupt")
finally:
    SEL.close()
