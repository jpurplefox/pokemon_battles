from dataclasses import dataclass


class UserEvent:
    pass


@dataclass
class PokemonUsedMove(UserEvent):
    battle_ref: str
    pokemon: str
    move: str
    damage: int


@dataclass
class BattleReady(UserEvent):
    battle_ref: str
