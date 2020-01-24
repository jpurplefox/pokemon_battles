from dataclasses import dataclass


class Event:
    pass


@dataclass(frozen=True)
class TurnReady(Event):
    battle_ref: str


@dataclass(frozen=True)
class TurnFinished(Event):
    battle_ref: str


@dataclass(frozen=True)
class MovePerformed(Event):
    battle_ref: str
    player: str
    pokemon_nickname: str
    move_name: str


@dataclass(frozen=True)
class OpponentMovePerformed(Event):
    battle_ref: str


@dataclass(frozen=True)
class PokemonChanged(Event):
    battle_ref: str
    player: str
    pokemon_nickname: str
