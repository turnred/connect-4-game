import json
import struct

class Messages:
    def _pack(message):
        json_msg = json.dumps(message).encode("utf-8")
        return struct.pack(f'<I{len(json_msg)}s', len(json_msg), json_msg)

    def msg_move(self, column):
        message = {
            "type": "moverequest",
            "column": column
        }
        return self._pack(message)

    def msg_username(self, username):
        message = {
            "type": "namerequest",
            "username": username
        }
        return self._pack(message)
