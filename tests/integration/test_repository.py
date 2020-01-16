from pokemon_battles.domain import models
from pokemon_battles.adapters import repositories

from ..random_refs import random_team_name


def test_get_team_by_name(mongo_database):
    repo = repositories.MongoTeamRepository(mongo_database)
    team_name_1, team_name_2 = random_team_name(), random_team_name()
    spark = models.Pokemon(
        'Spark',
        models.known_species['Pikachu'],
        level=20,
        moves=[models.known_moves['Thunder Shock']],
    )
    bubble = models.Pokemon(
        'Bubble',
        models.known_species['Squirtle'],
        level=20,
        moves=[models.known_moves['Bubble']],
    )
    team_1 = models.Team(team_name_1, pokemons=[spark])
    team_2 = models.Team(team_name_2, pokemons=[bubble])
    repo.add(team_1)
    repo.add(team_2)
    assert repo.get(team_name_1) == team_1
    assert repo.get(team_name_2) == team_2


def test_update_team(mongo_database):
    repo = repositories.MongoTeamRepository(mongo_database)
    team_name = random_team_name()
    spark = models.Pokemon(
        'Spark',
        models.known_species['Pikachu'],
        level=20,
        moves=[models.known_moves['Thunder Shock']],
    )
    team = models.Team(team_name)
    repo.add(team)
    assert repo.get(team_name) == team

    team.add_pokemon(spark)
    repo.update(team)
    assert repo.get(team_name) == team
