import struct
import json

class Messages:
    def _pack(message):
        json_msg = json.dumps(message).encode("utf-8")
        return struct.pack(f'<I{len(json_msg)}s', len(json_msg), json_msg)

    def msg_gamestatus(self, current_turn, turn_count, previous_move):
        message = {
            "type": "gamestatus",
            "current_turn": current_turn,
            "turn_count": turn_count,
            "prevmove": previous_move
        }
        return self._pack(message)

    def msg_gamestate(self, gamestate):
        message = {
            "type": "gamestate",
            "state": gamestate
        }
        return self._pack(message)
    
    def msg_gameover(self, winner):
        message = {
            "type": "gamestate",
            "state": "over",
            "winner": winner
        }
        return self._pack(message)

    def msg_move(self, valid_move):
        message = {
            "type": "moveresponse",
            "move": valid_move
        }
        return self._pack(message)

    def msg_acceptconn(self):
        message = {
            "type": "connresponse",
            "status": "accepted"
        }
        return self._pack(message)

    def msg_refuseconn(self, reason):
        message = {
            "type": "connresponse",
            "status": "refused",
            "reason": reason
        }
        return self._pack(message)
    
    def msg_nameaccept(self):
        message = {
            "type": "nameresponse",
            "status": "accepted"
        }
        return self._pack(message)
    
    def msg_namerefuse(self):
        message = {
            "type": "nameresponse",
            "status": "refused"
        }
