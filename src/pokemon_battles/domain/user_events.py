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


@dataclass
class BattleFinished(UserEvent):
    battle_ref: str
    winner: str


@dataclass
class TurnReady(UserEvent):
    battle_ref: str


@dataclass
class PokemonFainted(UserEvent):
    battle_ref: str
    pokemon: str


@dataclass
class PokemonChanged(UserEvent):
    battle_ref: str
    player: str
    pokemon_nickname: str
