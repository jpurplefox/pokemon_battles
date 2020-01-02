import models

def add_team(name, repository):
    team = models.Team(name)
    repository.add(team)

def add_pokemon_to_team(team_name, pokemon_nickname, pokemon_species, lvl, move_names, repository):
    moves = [models.known_moves[move_name] for move_name in move_names]

    pokemon = models.Pokemon(pokemon_nickname, models.known_species[pokemon_species], lvl, moves)
    team = repository.get(team_name)

    team.add_pokemon(pokemon)
