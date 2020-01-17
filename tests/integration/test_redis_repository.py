import uuid

from pokemon_battles.domain import models
from pokemon_battles.adapters import repositories

from ..random_refs import random_team_name


def test_get_team_by_name(redis_client):
    repo = repositories.RedisBattleRepository(redis_client)
    battle_ref = str(uuid.uuid4())
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
    team_1 = models.Team('Host', pokemons=[spark])
    team_2 = models.Team('Opponent', pokemons=[bubble])

    battle = models.Battle.host(battle_ref, team_1)
    repo.add(battle)

    assert repo.get(battle_ref) == battle

    battle.join(team_2)
    repo.update(battle)

    assert repo.get(battle_ref) == battle
