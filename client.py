import sys
import socket
import selectors

import libclient.message as message
import libclient.messages as messages

sel = selectors.DefaultSelector()

def start_connection(host, port):
    address = (host, port)
    print(f'Beginning connection to {address}')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.connect_ex(address)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(sock, events, data=message.Message(sel, sock, address, messages.start_conn()))
    
def get_action():
    while True:
        action = input("Enter an action")  
        if action != "move" or action != "set_name":
            print("Only move and set_name are supported")
        else:
            return action

if len(sys.argv) != 3:
    print("Please provide a host and a port")
    sys.exit(1)
host = sys.argv[1]
port = int(sys.argv[2])

start_connection(host, port)

try:
    while True:
        events = sel.select(timeout=1)
        if events:
            for key, mask in events:
                key.data.process_events(mask)
        if not sel.get_map():
         break
except KeyboardInterrupt:
    print("Gracefully exiting, keyboard interrupt")
finally:
    sel.close()
