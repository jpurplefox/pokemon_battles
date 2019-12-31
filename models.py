import math

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Species:
    name: str
    hp: int
    attack: int
    defense: int
    sp_attack: int
    sp_defense: int
    speed: int


@dataclass(frozen=True)
class Move:
    name: str
    power: int


class Pokemon:
    def __init__(self, nickname: str, species: Species, level: int, moves: set=None):
        self.nickname = nickname
        self.species = species
        self.level = level
        self.hp = self.max_hp
        self.moves = moves if moves else {}

    def _calculate_stats(self, base):
        return math.floor(5 + base * 2 * self.level / 100)

    @property
    def max_hp(self):
        return math.floor(10 + self.level + 2 * self.species.hp * self.level / 100)

    @property
    def attack(self):
        return self._calculate_stats(self.species.attack)

    @property
    def defense(self):
        return self._calculate_stats(self.species.defense)

    @property
    def sp_attack(self):
        return self._calculate_stats(self.species.sp_attack)

    @property
    def sp_defense(self):
        return self._calculate_stats(self.species.sp_defense)

    @property
    def speed(self):
        return self._calculate_stats(self.species.speed)

    def receive_damage(self, damage):
        self.hp = self.hp - damage

    def perform_move_against(self, move, other_pokemon):
        level_factor = 2 + 2 * self.level / 5
        attack_defense_ratio = self.attack / other_pokemon.defense
        damage = math.floor(level_factor * move.power * attack_defense_ratio / 50) + 2
        other_pokemon.receive_damage(damage)
        return damage
