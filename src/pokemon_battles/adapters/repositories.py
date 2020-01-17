import abc

from pokemon_battles.domain import models


class AbstractTeamRepository(abc.ABC):
    def __init__(self):
        self.seen = list()

    def add(self, team: models.Team):
        self._add(team)
        self.seen.append(team)

    def get(self, name: str):
        team = self._get(name)
        if team:
            self.seen.append(team)
        return team


class MongoTeamRepository(AbstractTeamRepository):
    def __init__(self, database):
        super().__init__()
        self.database = database

    @property
    def collection(self):
        return self.database.teams

    def update(self, team: models.Team):
        self.collection.replace_one({'name': team.name}, team.to_dict())

    def _add(self, team: models.Team):
        self.collection.insert_one(team.to_dict())

    def _get(self, name: str):
        raw_data = self.collection.find_one({'name': name})
        if not raw_data:
            return None
        return models.Team.from_dict(raw_data)


class AbstractBattleRepository(abc.ABC):
    def __init__(self):
        self.seen = set()

    def add(self, battle: models.Battle):
        self._add(battle)
        self.seen.add(battle)

    def get(self, battle_ref: str):
        battle = self._get(battle_ref)
        if battle:
            self.seen.add(battle)
        return battle


class RedisBattleRepository(AbstractBattleRepository):
    def _add(self, team: models.Team):
        pass

    def _get(self, name: str):
        pass
        if not raw_data:
            return None
        return models.Team.from_dict(raw_data)
