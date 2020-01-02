import uuid

import models

def add_team(name, uow):
    team = models.Team(name)
    with uow:
        uow.teams.add(team)
        uow.commit()

def add_pokemon_to_team(team_name, pokemon_nickname, pokemon_species, lvl, move_names, uow):
    moves = [models.known_moves[move_name] for move_name in move_names]

    pokemon = models.Pokemon(pokemon_nickname, models.known_species[pokemon_species], lvl, moves)
    with uow:
        team = uow.teams.get(team_name)
        team.add_pokemon(pokemon)
        uow.commit()

def host_battle(team_name, uow):
    ref = uuid.uuid4()
    with uow:
        team = uow.teams.get(team_name)
        uow.battles.add(models.Battle(ref, team))
    return ref

def join_battle(battle_ref, team_name, uow):
    with uow:
        team = uow.teams.get(team_name)
        battle = uow.battles.get(battle_ref)
        battle.join(team)
    return battle.host_team.name
