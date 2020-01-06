import commands
import repositories
from service_layer import messagebus
from service_layer.unit_of_work import AbstractUnitOfWork


class FakeTeamRepository:
    def __init__(self):
        self._teams = []

    def add(self, team):
        self._teams.append(team)

    def get(self, name):
        return next(team for team in self._teams if team.name == name)


class FakeBattleRepository(repositories.AbstractBattleRepository):
    def __init__(self):
        super().__init__()
        self._battles = []

    def _add(self, battle):
        self._battles.append(battle)

    def _get(self, ref):
        return next(battle for battle in self._battles if battle.ref == ref)


class FakeUnitOfWork(AbstractUnitOfWork):
    def __init__(self):
        self.init_repositories(FakeTeamRepository(), FakeBattleRepository())
        self.commited = False

    def _commit(self):
        self.commited = True

    def rollback(self):
        pass


def test_add_team():
    uow = FakeUnitOfWork()

    messagebus.handle(commands.AddTeam('My team'), uow)
    assert uow.teams.get('My team') is not None
    assert uow.commited


def test_add_pokemon_to_team():
    uow = FakeUnitOfWork()

    messagebus.handle(commands.AddTeam('My team'), uow)
    messagebus.handle(
        commands.AddPokemonToTeam('My team', 'Spark', 'pikachu', lvl=20, move_names=['thunder shock']),
        uow=uow
    )
    assert len(uow.teams.get('My team').pokemons) == 1


def create_a_battle(uow):
    messagebus.handle(commands.AddTeam('Host team'), uow)
    messagebus.handle(commands.AddTeam('Opponent team'), uow)

    messagebus.handle(
        commands.AddPokemonToTeam('Host team', 'Spark', 'pikachu', lvl=20, move_names=['thunder shock']),
        uow=uow
    )
    messagebus.handle(
        commands.AddPokemonToTeam('Opponent team', 'Bubble', 'squirtle', lvl=20, move_names=['bubble']),
        uow=uow
    )

    battle_ref = messagebus.handle(commands.HostBattle('Host team'), uow)

    messagebus.handle(commands.JoinBattle(battle_ref, 'Opponent team'), uow)

    return battle_ref


def test_host_and_join_a_battle():
    uow = FakeUnitOfWork()

    battle_ref = create_a_battle(uow)

    assert uow.battles.get(battle_ref) is not None


def test_a_battle_turn_is_successfully_complete():
    uow = FakeUnitOfWork()

    battle_ref = create_a_battle(uow)

    messagebus.handle(commands.RegisterHostMove(battle_ref, 'thunder shock'), uow)
    messagebus.handle(commands.RegisterOpponentMove(battle_ref, 'bubble'), uow)

    battle = uow.battles.get(battle_ref)

    assert battle.turn == 2
    assert battle.active_host_pokemon.hp < battle.active_host_pokemon.pokemon.max_hp
    assert battle.active_opponent_pokemon.hp < battle.active_opponent_pokemon.pokemon.max_hp


def test_opponent_can_choose_first_next_turn_move():
    uow = FakeUnitOfWork()

    battle_ref = create_a_battle(uow)

    messagebus.handle(commands.RegisterOpponentMove(battle_ref, 'bubble'), uow)

    battle = uow.battles.get(battle_ref)

    assert battle.turn == 1

    messagebus.handle(commands.RegisterHostMove(battle_ref, 'thunder shock'), uow)

    assert battle.turn == 2
