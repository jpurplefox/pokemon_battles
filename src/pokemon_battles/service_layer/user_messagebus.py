import abc

from flask_socketio import SocketIO

from pokemon_battles.domain import user_events


class AbstractUserMessagebus(abc.ABC):
    pass

    @abc.abstractmethod
    def emit(self, event: user_events.UserEvent):
        raise NotImplementedError


class FlaskSocketIOUserMessagebus(AbstractUserMessagebus):
    def __init__(self, message_queue):
        self.socketio = SocketIO(message_queue=message_queue)

    def emit(self, event: user_events.UserEvent):
        self.socketio.emit('move', {'pokemon': event.pokemon}, room=event.battle_ref)
