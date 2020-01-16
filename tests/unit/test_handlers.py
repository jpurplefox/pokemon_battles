from pokemon_battles.adapters import repositories
from pokemon_battles.domain import commands, user_events
from pokemon_battles.service_layer import messagebus
from pokemon_battles.service_layer.unit_of_work import AbstractUnitOfWork
from pokemon_battles.service_layer.user_messagebus import AbstractUserMessagebus


class FakeTeamRepository(repositories.AbstractTeamRepository):
    def __init__(self):
        super().__init__()
        self._teams = []

    def _add(self, team):
        self._teams.append(team)

    def _get(self, name):
        return next(team for team in self._teams if team.name == name)


class FakeBattleRepository(repositories.AbstractBattleRepository):
    def __init__(self):
        super().__init__()
        self._battles = []

    def _add(self, battle):
        self._battles.append(battle)

    def _get(self, ref):
        return next(battle for battle in self._battles if battle.ref == ref)


class FakeUserMessagebus(AbstractUserMessagebus):
    def __init__(self):
        self.events = []

    def emit(self, event):
        self.events.append(event)


class FakeUnitOfWork(AbstractUnitOfWork):
    def __init__(self):
        self.init_repositories(FakeTeamRepository(), FakeBattleRepository())
        self.user_messagebus = FakeUserMessagebus()
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
        commands.AddPokemonToTeam('My team', 'Spark', 'Pikachu', lvl=20, move_names=['Thunder Shock']),
        uow=uow
    )
    assert len(uow.teams.get('My team').pokemons) == 1


def create_a_battle(uow):
    messagebus.handle(commands.AddTeam('Host team'), uow)
    messagebus.handle(commands.AddTeam('Opponent team'), uow)

    messagebus.handle(
        commands.AddPokemonToTeam('Host team', 'Spark', 'Pikachu', lvl=20, move_names=['Thunder Shock']),
        uow=uow
    )
    messagebus.handle(
        commands.AddPokemonToTeam('Opponent team', 'Bubble', 'Squirtle', lvl=20, move_names=['Bubble']),
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

    messagebus.handle(commands.RegisterHostMove(battle_ref, 'Thunder Shock'), uow)
    messagebus.handle(commands.RegisterOpponentMove(battle_ref, 'Bubble'), uow)

    battle = uow.battles.get(battle_ref)

    expected_events = [
        user_events.PokemonUsedMove(battle_ref, 'Pikachu', 'Thunder Shock', 8),
        user_events.PokemonUsedMove(battle_ref, 'Squirtle', 'Bubble', 13),
    ]

    assert uow.user_messagebus.events == expected_events


def test_opponent_can_choose_first_next_turn_move():
    uow = FakeUnitOfWork()

    battle_ref = create_a_battle(uow)

    messagebus.handle(commands.RegisterOpponentMove(battle_ref, 'Bubble'), uow)

    assert uow.user_messagebus.events == []

    messagebus.handle(commands.RegisterHostMove(battle_ref, 'Thunder Shock'), uow)

    expected_events = [
        user_events.PokemonUsedMove(battle_ref, 'Pikachu', 'Thunder Shock', 8),
        user_events.PokemonUsedMove(battle_ref, 'Squirtle', 'Bubble', 13),
    ]

    assert uow.user_messagebus.events == expected_events
