import math
from dataclasses import dataclass

import events


@dataclass(frozen=True)
class Species:
    name: str
    hp: int
    attack: int
    defense: int
    sp_attack: int
    sp_defense: int
    speed: int


known_species = {
    'squirtle': Species(
        'Squirtle',
        hp=44,
        attack=48,
        defense=65,
        sp_attack=50,
        sp_defense=64,
        speed=43,
    ),
    'pikachu': Species(
        'Pikachu',
        hp=35,
        attack=55,
        defense=30,
        sp_attack=50,
        sp_defense=40,
        speed=90,
    ),
}


@dataclass(frozen=True)
class Move:
    name: str
    power: int


known_moves = {
    'thunder shock': Move('Thunder Shock', 40),
    'bubble': Move('Bubble', 40),
}


class Pokemon:
    def __init__(self, nickname: str, species: Species, level: int, moves: set=None):
        self.nickname = nickname
        self.species = species
        self.level = level
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


class Team:
    def __init__(self, name):
        self.name = name
        self._pokemons = []

    def add_pokemon(self, pokemon: Pokemon):
        self._pokemons.append(pokemon)

    @property
    def pokemons(self):
        return self._pokemons


class Battle:
    def __init__(self, ref: str, host_team: Team):
        self.ref = ref

        self.host_pokemons = [BattlingPokemon(pokemon) for pokemon in host_team.pokemons]
        self.host_pokemons[0].is_active = True

        self.opponent_pokemons = None

        self.turn = 1
        self.events = []

    def join(self, opponent_team):
        self.opponent_pokemons = [BattlingPokemon(pokemon) for pokemon in opponent_team.pokemons]
        self.opponent_pokemons[0].is_active = True

    @property
    def active_host_pokemon(self):
        return next(pokemon for pokemon in self.host_pokemons if pokemon.is_active)

    @property
    def active_opponent_pokemon(self):
        return next(pokemon for pokemon in self.opponent_pokemons if pokemon.is_active)

    def register_host_move(self, move: Move):
        self.active_host_pokemon.next_move = move
        if self.active_opponent_pokemon.next_move:
            self.events.append(events.TurnReady(self.ref))

    def register_opponent_move(self, move: Move):
        self.active_opponent_pokemon.next_move = move
        if self.active_host_pokemon.next_move:
            self.events.append(events.TurnReady(self.ref))

    def process_turn(self):
        self.turn = self.turn + 1
        self.events.append(events.HostMovePerformed(self.ref))
        self.active_opponent_pokemon.perform_move_against(self.active_host_pokemon)

    def perform_host_move(self):
        pokemon_that_moved = next(pokemon for pokemon in self.host_pokemons if pokemon.next_move)
        if pokemon_that_moved.is_active:
            pokemon_that_moved.perform_move_against(self.active_opponent_pokemon)
        pokemon_that_moved.next_move = None

    def perform_opponent_move(self):
        pokemon_that_moved = next(pokemon for pokemon in self.opponent_pokemons if pokemon.next_move)
        if pokemon_that_moved.is_active:
            pokemon_that_moved.perform_move_against(self.active_host_pokemon)
        pokemon_that_moved.next_move = None


class BattlingPokemon:
    def __init__(self, pokemon: Pokemon):
        self.pokemon = pokemon
        self.hp = pokemon.max_hp
        self.is_active = False
        self.next_move = None

    def receive_damage(self, damage):
        self.hp = self.hp - damage

    def perform_move_against(self, other_pokemon):
        level_factor = 2 + 2 * self.pokemon.level / 5
        attack_defense_ratio = self.pokemon.attack / other_pokemon.pokemon.defense
        damage = math.floor(level_factor * self.next_move.power * attack_defense_ratio / 50) + 2
        other_pokemon.receive_damage(damage)
