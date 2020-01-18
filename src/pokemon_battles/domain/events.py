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
class HostMovePerformed(Event):
    battle_ref: str


@dataclass(frozen=True)
class OpponentMovePerformed(Event):
    battle_ref: str
