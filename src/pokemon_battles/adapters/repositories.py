import abc
import json

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
        self.seen = list()

    def add(self, battle: models.Battle):
        self._add(battle)
        self.seen.append(battle)

    def get(self, battle_ref: str):
        battle = self._get(battle_ref)
        if battle:
            self.seen.append(battle)
        return battle


class RedisBattleRepository(AbstractBattleRepository):
    def __init__(self, client):
        super().__init__()
        self.client = client

    def get_key(self, ref):
        return f'battle-{ref}'

    def update(self, team: models.Team):
        self.client.set(self.get_key(team.ref), json.dumps(team.to_dict()))

    def _add(self, team: models.Team):
        self.client.set(self.get_key(team.ref), json.dumps(team.to_dict()))

    def _get(self, ref: str):
        raw_data = json.loads(self.client.get(self.get_key(ref)))
        if not raw_data:
            return None
        return models.Battle.from_dict(raw_data)
