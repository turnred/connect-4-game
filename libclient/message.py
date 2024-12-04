import selectors
import struct
import json
import io
import sys

from libclient.messages import *

class Message:
    def __init__(self, sock):
        self.sel = selectors.DefaultSelector()
        self.sock = sock
        self.messages = Messages()
    
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
        self.sel.modify(self.sock, events, data=self)

    def handle_listener(self, message):
        """Logic the client receives a response"""
        type = message.get("type")
        if type == "connresponse":
            if message.get("status") == "refused":
                reason = message.get("reason")
                print(f'Connected refused, server returned {reason}')
                exit(0)
            else:
                print(f'Connection to server accepted')
            return
        if type == "gamestate":
            if message.get("state") == "waiting":
                username = input("Please input a username")
                self.write(self.messages.msg_username(username, self.sock))
            elif message.get("state") == "in progress":
                self.board == message.get("board")
                self.print_board()
        if type == "moveresponse":
            if message.get("move") == False:
                print(f'Server returned move as invalid')
                column = input("Input a move")
                self.write(self.messages.msg_move(column), self.sock)
            elif message.get("move") == True:
                self.print_board()

    def print_board(self):
        """Prints the gameboard"""
        print("\n")
        for row in self.board:
            print(" ".join(row))
        print("\n\n\n")
            
    def write(self, message, sock):
        """Writes data to the server"""
        print(f'Writing data {message} to server')
        sock.sendall(message)
