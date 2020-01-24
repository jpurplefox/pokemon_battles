import logging
from typing import Union

from pokemon_battles.domain import commands, events
from . import handlers

logger = logging.getLogger(__name__)

Message = Union[commands.Command, events.Event]


def handle(message: Message, uow):
    if isinstance(message, events.Event):
        handle_event(message, uow)
    elif isinstance(message, commands.Command):
        return handle_command(message, uow)
    else:
        raise Exception(f'{message} was not an Event or Command')


def handle_event(event: events.Event, uow):
    for handler in EVENT_HANDLERS[type(event)]:
        try:
            logger.debug('handling event %s with handler %s', event, handler)
            handler(event, uow=uow)
        except:
            logger.exception('Exception handling event %s', event)
            raise


def handle_command(command, uow):
    logger.debug('handling command %s', command)
    try:
        handler = COMMAND_HANDLERS[type(command)]
        return handler(command, uow=uow)
    except Exception:
        logger.exception('Exception handling command %s', command)
        raise


EVENT_HANDLERS = {
    events.MovePerformed: [handlers.move_performed],
    events.PokemonChanged: [handlers.pokemon_changed],
    events.TurnReady: [handlers.turn_ready],
    events.TurnFinished: [handlers.turn_finished],
}


COMMAND_HANDLERS = {
    commands.AddPokemonToTeam: handlers.add_pokemon_to_team,
    commands.AddTeam: handlers.add_team,
    commands.HostBattle: handlers.host_battle,
    commands.JoinBattle: handlers.join_battle,
    commands.RegisterUseMove: handlers.register_use_move,
    commands.RegisterChangePokemon: handlers.register_change_pokemon,
}
