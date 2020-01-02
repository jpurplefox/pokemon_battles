import pytest

import services
from unit_of_work import AbstractUnitOfWork


class FakeTeamRepository:
    def __init__(self):
        self._teams = []

    def add(self, team):
        self._teams.append(team)

    def get(self, name):
        return next(team for team in self._teams if team.name == name)


class FakeBattleRepository:
    def __init__(self):
        self._battles = []

    def add(self, battle):
        self._battles.append(battle)

    def get(self, ref):
        return next(battle for battle in self._battles if battle.ref == ref)


class FakeUnitOfWork(AbstractUnitOfWork):
    def __init__(self):
        self.init_repositories(FakeTeamRepository(), FakeBattleRepository())
        self.commited = False

    def commit(self):
        self.commited = True

    def rollback(self):
        pass


def test_add_team():
    uow = FakeUnitOfWork()

    services.add_team('My team', uow)
    assert uow.teams.get('My team') is not None
    assert uow.commited

def test_add_pokemon_to_team():
    uow = FakeUnitOfWork()

    services.add_team('My team', uow)
    services.add_pokemon_to_team(
        'My team', 'Spark', 'pikachu', lvl=20, move_names=['thunder shock'],
        uow=uow
    )
    assert len(uow.teams.get('My team').pokemons) == 1

def test_host_a_battle():
    uow = FakeUnitOfWork()

    services.add_team('My team', uow)
    services.add_pokemon_to_team(
        'My team', 'Spark', 'pikachu', lvl=20, move_names=['thunder shock'],
        uow=uow
    )

    battle_ref = services.host_battle('My team', uow)

    assert uow.battles.get(battle_ref) is not None

def test_join_a_battle():
    uow = FakeUnitOfWork()

    services.add_team('Host team', uow)
    services.add_pokemon_to_team(
        'Host team', 'Spark', 'pikachu', lvl=20, move_names=['thunder shock'],
        uow=uow
    )

    battle_ref = services.host_battle('Host team', uow)

    services.add_team('Opponent team', uow)
    services.add_pokemon_to_team(
        'Opponent team', 'Bubble', 'squirtle', lvl=20, move_names=['bubble'],
        uow=uow
    )

    host_team = services.join_battle(battle_ref, 'Opponent team', uow)

    assert host_team == 'Host team'
