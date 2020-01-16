import abc

from pokemon_battles.domain import models


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
