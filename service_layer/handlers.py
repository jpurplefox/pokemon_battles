import uuid

import commands
import events
import models


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
    ref = uuid.uuid4()
    with uow:
        team = uow.teams.get(cmd.team_name)
        uow.battles.add(models.Battle(ref, team))
        uow.commit()
    return ref


def join_battle(cmd: commands.JoinBattle, uow):
    with uow:
        team = uow.teams.get(cmd.team_name)
        battle = uow.battles.get(cmd.battle_ref)
        battle.join(team)
        uow.commit()


def register_host_move(cmd: commands.RegisterHostMove, uow):
    with uow:
        battle = uow.battles.get(cmd.battle_ref)
        move = models.known_moves[cmd.move_name]
        battle.register_host_move(move)
        uow.commit()


def register_opponent_move(cmd: commands.RegisterOpponentMove, uow):
    with uow:
        battle = uow.battles.get(cmd.battle_ref)
        move = models.known_moves[cmd.move_name]
        battle.register_opponent_move(move)
        uow.commit()


def turn_ready(event: events.TurnReady, uow):
    with uow:
        battle = uow.battles.get(event.battle_ref)
        battle.process_turn()
        uow.commit()
