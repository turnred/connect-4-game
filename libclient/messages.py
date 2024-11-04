import json
import struct

def _pack(message):
    bytes_msg = _json_encode(message, "utf-8")
    return struct.pack(f'<i{len(bytes_msg)}s', len(bytes_msg), bytes_msg)

def _json_encode(self, obj, encoding):
    return json.dumps(obj, ensure_ascii=False).encode(encoding)

def start_conn():
    message = {
        "message": "connect"
    }
    return _pack(message)

def move():
    message = {
        "message": "move"
    }
    return _pack(message)

def change_name():
    message = {
        "message": "username"
    }
    return _pack(message)
