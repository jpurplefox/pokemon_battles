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
        if isinstance(event, user_events.BattleReady):
            self.socketio.emit('battle_ready', {'battle_ref': event.battle_ref}, room=event.battle_ref)
        if isinstance(event, user_events.PokemonUsedMove):
            self.socketio.emit('move', {'pokemon': event.pokemon, 'move': event.move}, room=event.battle_ref)
        if isinstance(event, user_events.TurnReady):
            self.socketio.emit('turn_ready', {'battle_ref': event.battle_ref}, room=event.battle_ref)
