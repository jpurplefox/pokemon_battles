import pytest

import commands
from service_layer import messaggebus
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

    messaggebus.handle(commands.AddTeam('My team'), uow)
    assert uow.teams.get('My team') is not None
    assert uow.commited

def test_add_pokemon_to_team():
    uow = FakeUnitOfWork()

    messaggebus.handle(commands.AddTeam('My team'), uow)
    messaggebus.handle(
        commands.AddPokemonToTeam('My team', 'Spark', 'pikachu', lvl=20, move_names=['thunder shock']),
        uow=uow
    )
    assert len(uow.teams.get('My team').pokemons) == 1

def test_host_a_battle():
    uow = FakeUnitOfWork()

    messaggebus.handle(commands.AddTeam('My team'), uow)
    messaggebus.handle(
        commands.AddPokemonToTeam('My team', 'Spark', 'pikachu', lvl=20, move_names=['thunder shock']),
        uow=uow
    )

    battle_ref = messaggebus.handle(commands.HostBattle('My team'), uow)

    assert uow.battles.get(battle_ref) is not None

def test_join_a_battle():
    uow = FakeUnitOfWork()

    messaggebus.handle(commands.AddTeam('Host team'), uow)
    messaggebus.handle(commands.AddTeam('Opponent team'), uow)

    messaggebus.handle(
        commands.AddPokemonToTeam('Host team', 'Spark', 'pikachu', lvl=20, move_names=['thunder shock']),
        uow=uow
    )
    messaggebus.handle(
        commands.AddPokemonToTeam('Opponent team', 'Bubble', 'squirtle', lvl=20, move_names=['bubble']),
        uow=uow
    )

    battle_ref = messaggebus.handle(commands.HostBattle('Host team'), uow)

    host_team = messaggebus.handle(commands.JoinBattle(battle_ref, 'Opponent team'), uow)

    assert host_team == 'Host team'
