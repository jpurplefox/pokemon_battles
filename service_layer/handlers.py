import uuid

import commands
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
    return ref


def join_battle(cmd: commands.JoinBattle, uow):
    with uow:
        team = uow.teams.get(cmd.team_name)
        battle = uow.battles.get(cmd.battle_ref)
        battle.join(team)
    return battle.host_team.name
