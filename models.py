import math

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Move:
    name: str
    power: int


@dataclass
class Pokemon:
    nickname: str
    hp: int
    attack: int
    defense: int
    moves: set = field(default_factory=set)

    def receive_damage(self, damage):
        self.hp = self.hp - damage

    def perform_move_against(self, move, other_pokemon):
        damage = math.floor(move.power * self.attack / other_pokemon.defense) + 2
        other_pokemon.receive_damage(damage)
        return damage
