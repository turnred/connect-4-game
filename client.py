import sys
import socket
import selectors
import types

SEL = selectors.DefaultSelector()

def start_connection(host, port, num_connections):
    address = (host, port)
    for i in range(num_connections):
        print("Beginning connection to ", address)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(address)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        data = types.SimpleNamespace(connid=i+1, msg_total=5, recv_total=0, messages=b"Test",outb=b"",)
        SEL.register(sock, events, data=data)

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data is not None:
            data.recv_total += len(recv_data)
            print("Data ", repr(recv_data), "received from connection ", data.connid)
        if not recv_data or data.recv_total == data.msg_total:
            SEL.unregister(sock)
            sock.close()
            print(data.connid, " connection closed")
    if mask & selectors.EVENT_WRITE:
        if not data.outb and data.messages:
            data.outb = data.messages.pop(0)
        if data.outb:
            sent = sock.send(data.outb)
            data.outb = data.outb[sent:]
            print("Data ", repr(data.outb), "sent to connection ", data.connid)

host = '0.0.0.0'
port = 35565
num_connections = 2

start_connection(host, port, num_connections)

try:
    while True:
    events = SEL.select(timeout=None)
    if events:
        for key, mask in events:
            service_connection(key, mask)
    if not SEL.get_map():
        break
except KeyboardInterrupt:
    print("Gracefully exiting, keyboard interrupt")
finally:
    SEL.close()
