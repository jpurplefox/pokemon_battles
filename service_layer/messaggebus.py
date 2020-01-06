import logging

import commands
from . import handlers

logger = logging.getLogger(__name__)


def handle(message, uow):
    return handle_command(message, uow)


def handle_command(command, uow):
    logger.debug('handling command %s', command)
    try:
        handler = COMMAND_HANDLERS[type(command)]
        return handler(command, uow=uow)
    except Exception:
        logger.exception('Exception handling command %s', command)
        raise


COMMAND_HANDLERS = {
    commands.AddPokemonToTeam: handlers.add_pokemon_to_team,
    commands.AddTeam: handlers.add_team,
    commands.HostBattle: handlers.host_battle,
    commands.JoinBattle: handlers.join_battle,
}
