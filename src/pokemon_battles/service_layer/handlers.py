import uuid

from pokemon_battles.domain import commands, events, models


def add_team(cmd: commands.AddTeam, uow):
    team = models.Team(cmd.name)
    with uow:
        uow.teams.add(team)
        uow.commit()


def add_pokemon_to_team(cmd: commands.AddPokemonToTeam, uow):
    moves = [models.known_moves[move_name] for move_name in cmd.move_names]

    pokemon = models.Pokemon(cmd.nickname, models.known_species[cmd.species], cmd.lvl, moves)
    with uow:
        team = uow.teams.get(cmd.team_name)
        team.add_pokemon(pokemon)
        uow.commit()


def host_battle(cmd: commands.HostBattle, uow):
    ref = str(uuid.uuid4())
    with uow:
        team = uow.teams.get(cmd.team_name)
        uow.battles.add(models.Battle.host(ref, team))
        uow.commit()
    return ref


def join_battle(cmd: commands.JoinBattle, uow):
    with uow:
        team = uow.teams.get(cmd.team_name)
        battle = uow.battles.get(cmd.battle_ref)
        battle.join(team)
        uow.commit()


def register_use_move(cmd: commands.RegisterUseMove, uow):
    with uow:
        battle = uow.battles.get(cmd.battle_ref)
        battle.register_use_move(cmd.player, cmd.move_name)
        uow.commit()


def register_change_pokemon(cmd: commands.RegisterChangePokemon, uow):
    with uow:
        battle = uow.battles.get(cmd.battle_ref)
        battle.register_change_pokemon(cmd.player, cmd.pokemon_nickname)
        uow.commit()


def move_performed(event: events.MovePerformed, uow):
    with uow:
        battle = uow.battles.get(event.battle_ref)
        battle.perform_move(event.player, event.pokemon_nickname, event.move_name)
        uow.commit()


def pokemon_changed(event: events.PokemonChanged, uow):
    with uow:
        battle = uow.battles.get(event.battle_ref)
        battle.change_pokemon(event.player, event.pokemon_nickname)
        uow.commit()


def turn_ready(event: events.TurnReady, uow):
    with uow:
        battle = uow.battles.get(event.battle_ref)
        battle.process_turn()
        uow.commit()


def turn_finished(event: events.TurnFinished, uow):
    with uow:
        battle = uow.battles.get(event.battle_ref)
        battle.finish_turn()
        uow.commit()
