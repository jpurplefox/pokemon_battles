import services


class FakeRepository:
    def __init__(self):
        self._teams = []

    def add(self, team):
        self._teams.append(team)

    def get(self, name):
        return next(team for team in self._teams if team.name == name)


def test_add_team():
    repository = FakeRepository()

    services.add_team('My team', repository)
    assert repository.get('My team') is not None

def test_add_pokemon_to_team():
    repository = FakeRepository()

    services.add_team('My team', repository)
    services.add_pokemon_to_team(
        'My team', 'Spark', 'pikachu', lvl=20, move_names=['thunder shock'],
        repository=repository
    )
    assert len(repository.get('My team').pokemons) == 1
