import selectors
import struct
import json
import io

import libserver.messages as messages

class Message:
    def __init__(self, selector, sock, address):
        self.selector = selector
        self.sock = sock
        self.address = address

    def _json_decode(self, json_bytes, encoding):
        """returns a decoded json object from encoding: utf-8."""
        tiow = io.TextIOWrapper(
            io.BytesIO(json_bytes), encoding=encoding, newline=""
        )
        obj = json.load(tiow)
        tiow.close()
        return obj
    
    def _set_selector_events_mask(self, mode):
        """Set selector to listen for events: mode is 'r', 'w', or 'rw'."""
        if mode == "r":
            events = selectors.EVENT_READ
        elif mode == "w":
            events = selectors.EVENT_WRITE
        elif mode == "rw":
            events = selectors.EVENT_READ | selectors.EVENT_WRITE
        else:
            raise ValueError(f"Invalid events mask mode {repr(mode)}.")
        self.selector.modify(self.sock, events, data=self)
    
    def process_events(self, mask):
        if mask & selectors.EVENT_READ:
            self.read()
        if mask & selectors.EVENT_WRITE:
            self.write()
    
    def read(self):
        data_buffer = self.sock.recv(4)
        if data_buffer:
            length = struct.unpack('<i', data_buffer)
            data = self.sock.recv(length[0])
            print(f'Received data length of {length} bytes')
            message = self._json_decode(data, "utf-8").get("message")
            if message == "username":
                #users.setname()
                self.write(messages.conn_ok, self.sock)
            if message == "move":
                move = messages.move()
                self.write(move, self.sock)
                self.write_all(messages.board)

    def write(self, message, sock):
        print(f'Wrote data to client')
        sock.sendall(message)
    
    def write_all(self, message):
        for user in user.get_user():
            user.sock.send(message)
