import struct
import json

def _pack(message):
    bytes_msg = _json_encode(message, "utf-8")
    return struct.pack(f'<i{len(bytes_msg)}s', len(bytes_msg), bytes_msg)

def _json_encode(self, obj, encoding):
    return json.dumps(obj, ensure_ascii=False).encode(encoding)

def conn_refuse():
    message = {
        "message": "refused"
    }
    return _pack(message)

def conn_wait():
    message = {
        "message": "wait"
    }
    return _pack(message)

def move():
    #TODO: game logic to check for valid move
    if (True):
        message = {
            "message": "accepted"
        }
        return _pack(message)
    
def board():
    #TODO: needs a board to return
    message = {
        "message": "board"
    }
    return _pack(message)

def end_game():
    #TODO: update to support a winner
    message = {
        "message": "gameover"
    }
    return _pack(message)
