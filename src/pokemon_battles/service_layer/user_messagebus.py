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
            event_name = 'battle_ready'
            data = {'battle_ref': event.battle_ref}
        if isinstance(event, user_events.BattleFinished):
            event_name = 'battle_finished'
            data = {'winner': event.winner}
        if isinstance(event, user_events.PokemonUsedMove):
            event_name = 'move'
            data = {'pokemon': event.pokemon, 'move': event.move}
        if isinstance(event, user_events.PokemonChanged):
            event_name = 'pokemon_changed'
            data = {'player': event.player, 'pokemon_nickname': event.pokemon_nickname}
        if isinstance(event, user_events.TurnReady):
            event_name = 'turn_ready'
            data = {'battle_ref': event.battle_ref}
        if isinstance(event, user_events.PokemonFainted):
            event_name = 'pokemon_fainted'
            data = {'pokemon': event.pokemon}
        self.socketio.emit(event_name, data, room=event.battle_ref)
