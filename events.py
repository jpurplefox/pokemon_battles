from dataclasses import dataclass


class Event:
    pass


@dataclass(frozen=True)
class TurnReady(Event):
    battle_ref: str
