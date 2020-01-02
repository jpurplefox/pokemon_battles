import services


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


def test_add_team():
    repository = FakeTeamRepository()

    services.add_team('My team', repository)
    assert repository.get('My team') is not None

def test_add_pokemon_to_team():
    repository = FakeTeamRepository()

    services.add_team('My team', repository)
    services.add_pokemon_to_team(
        'My team', 'Spark', 'pikachu', lvl=20, move_names=['thunder shock'],
        repository=repository
    )
    assert len(repository.get('My team').pokemons) == 1

def test_host_a_battle():
    team_repository = FakeTeamRepository()
    battle_repository = FakeBattleRepository()

    services.add_team('My team', team_repository)
    services.add_pokemon_to_team(
        'My team', 'Spark', 'pikachu', lvl=20, move_names=['thunder shock'],
        repository=team_repository
    )

    battle_ref = services.host_battle('My team', team_repository, battle_repository)

    assert battle_repository.get(battle_ref) is not None

def test_join_a_battle():
    team_repository = FakeTeamRepository()
    battle_repository = FakeBattleRepository()

    services.add_team('Host team', team_repository)
    services.add_pokemon_to_team(
        'Host team', 'Spark', 'pikachu', lvl=20, move_names=['thunder shock'],
        repository=team_repository
    )

    battle_ref = services.host_battle('Host team', team_repository, battle_repository)

    services.add_team('Opponent team', team_repository)
    services.add_pokemon_to_team(
        'Opponent team', 'Bubble', 'squirtle', lvl=20, move_names=['bubble'],
        repository=team_repository
    )

    services.join_battle(battle_ref, 'Opponent team', team_repository, battle_repository)
