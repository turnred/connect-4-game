import selectors
import struct
import json
import io

from libserver.user import *
from libserver.messages import *
from libserver.game import *

class Message:
    def __init__(self, sel, connected):
        self.sel = sel
        self.connected = connected
        self.users = {}
        self.messages = Messages()

    def _json_decode(self, json_bytes):
        """returns a decoded json object from encoding: utf-8."""
        json_msg = json.loads(json_bytes)
        return json_msg
    
    def read(self, sock):
        """Reads data from clients"""
        data_buffer = sock.recv(4)
        if data_buffer:
            length = struct.unpack('<i', data_buffer)
            data = sock.recv(length[0])
            print(f'Received data of length {length}')
            message = self._json_decode(data)
            self.action_handler(message, sock)

    def action_handler(self, message, sock):
        """Upon receiving a JSON request, handles it"""
        action = message.get("type")
        if action is None:
            return
        if action == "namerequest":
            self.set_username(sock, message)
        if action == "moverequest":
            self.move_handler()        

    def set_username(self, sock, message):
        """Sets a client's username"""
        username = message.get("username")
        if username:
            address = self.connected.get(sock)
            self.users[address].set_name(username)
            self.write(Messages.msg_nameaccept(), sock)
        else:
            self.write(Messages.msg_namerefuse(), sock)
        if self.both_users_connected():
            self.game = Game(self.users)
            self.writeall(Messages.msg_gamestate("in progress"))

    def both_users_connected(self):
        """Utility for if a game can begin"""
        for user in self.users:
            if user.name is None:
                return False
        return True
    
    def move_handler(self, message, sock):
        """Checks if a move is valid, returns JSON to the client"""
        if not self.game:
            self.writeall(Messages.msg_gamestate("waiting"))
            return
        moveto = message.get("column")
        if self.game.draw_check() is True:
            self.writeall(Messages.msg_gameover("None"))
        if moveto:
            if self.game.bounds_check(moveto) is True:
                self.game.move(moveto)
                self.game.switch_turn()
                self.write(Messages.msg_move(True), sock)
                winner = self.game.check_winner()
                if winner:
                    self.writeall(Messages.msg_gameover(winner))
                else:
                    self.writeall(Messages.msg_gamestatus(self.game.current_turn, self.game.turn_count, moveto))
            else:
                self.write(Messages.msg_move(False), sock)
    
    def create_user(self, address):
        """Users are a dictionary of addresses and usernames"""
        self.users[address] = User(address)

    def write(self, message, sock):
        """Writes data to the client"""
        print("Wrote data to client", sock)
        sock.sendall(message)
    
    def writeall(self, message):
        """Writes data to all clients"""
        for sock in self.connected:
            self.write(message, sock)
