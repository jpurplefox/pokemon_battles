from flask_socketio import SocketIO

import user_events
from pokemon_battles.service_layer.user_messagebus import AbstractUserMessagebus


class FlaskSocketIOUserMessagebus(AbstractUserMessagebus):
    def __init__(self, message_queue):
        self.socketio = SocketIO(message_queue=message_queue)

    def emit(self, event: user_events.UserEvent):
        self.socketio.emit('move', {'pokemon': event.pokemon}, room=event.battle_ref)
