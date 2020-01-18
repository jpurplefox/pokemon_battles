import math

from dataclasses import dataclass, field
from typing import List, Set

from . import events, user_events


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
    'Squirtle': Species(
        'Squirtle',
        hp=44,
        attack=48,
        defense=65,
        sp_attack=50,
        sp_defense=64,
        speed=43,
    ),
    'Pikachu': Species(
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
    'Thunder Shock': Move('Thunder Shock', 40),
    'Bubble': Move('Bubble', 40),
}


@dataclass
class Pokemon:
    nickname: str
    species: Species
    level: int
    moves: Set[Move] = field(default_factory=set)

    def to_dict(self):
        return {
            'nickname': self.nickname,
            'species': self.species.name,
            'level': self.level,
            'moves': [move.name for move in self.moves],
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            nickname=data['nickname'],
            species=known_species[data['species']],
            level=data['level'],
            moves=[known_moves[move] for move in data.get('moves', [])],
        )

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


@dataclass
class Team:
    name: str
    pokemons: List[Pokemon] = field(default_factory=list)

    def add_pokemon(self, pokemon: Pokemon):
        self.pokemons.append(pokemon)

    def to_dict(self):
        return {
            'name': self.name,
            'pokemons': [pokemon.to_dict() for pokemon in self.pokemons]
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data['name'],
            pokemons=[Pokemon.from_dict(pokemon_data) for pokemon_data in data.get('pokemons', [])]
        )


@dataclass
class BattlingPokemon:
    pokemon: Pokemon
    hp: int = 0
    is_active: bool = False
    next_move: Move = None

    def to_dict(self):
        if self.next_move:
            move_name = self.next_move.name
        else:
            move_name = None

        return {
            'pokemon': self.pokemon.to_dict(),
            'hp': self.hp,
            'is_active': self.is_active,
            'next_move': move_name
        }

    @classmethod
    def from_dict(cls, data):
        if move_name := data.get('next_move', None):
            next_move = known_moves[move_name]
        else:
            next_move = None

        return cls(
            pokemon=Pokemon.from_dict(data['pokemon']),
            hp=data['hp'],
            is_active=data['is_active'],
            next_move=next_move,
        )

    def receive_damage(self, damage):
        self.hp = self.hp - damage

    def perform_move_against(self, other_pokemon):
        level_factor = 2 + 2 * self.pokemon.level / 5
        attack_defense_ratio = self.pokemon.attack / other_pokemon.pokemon.defense
        damage = math.floor(level_factor * self.next_move.power * attack_defense_ratio / 50) + 2
        other_pokemon.receive_damage(damage)

        return damage


@dataclass
class Battle:
    ref: str
    host_pokemons: List[BattlingPokemon]
    opponent_pokemons: List[BattlingPokemon] = field(default_factory=list)

    events: list = field(default_factory=list, repr=False, compare=False)
    user_events: list = field(default_factory=list, repr=False, compare=False)

    def to_dict(self):
        return {
            'ref': self.ref,
            'host_pokemons': [pokemon.to_dict() for pokemon in self.host_pokemons],
            'opponent_pokemons': [pokemon.to_dict() for pokemon in self.opponent_pokemons],
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            ref=data['ref'],
            host_pokemons=[
                BattlingPokemon.from_dict(pokemon) for pokemon in data.get('host_pokemons', [])
            ],
            opponent_pokemons=[
                BattlingPokemon.from_dict(pokemon) for pokemon in data.get('opponent_pokemons', [])
            ],
        )

    @classmethod
    def host(cls, ref: str, host_team: Team):
        battle = cls(
            ref,
            [BattlingPokemon(pokemon, pokemon.max_hp) for pokemon in host_team.pokemons],
        )
        battle.host_pokemons[0].is_active = True

        battle.events = []
        battle.user_events = []
        return battle

    def join(self, opponent_team):
        self.opponent_pokemons = [
            BattlingPokemon(pokemon, pokemon.max_hp) for pokemon in opponent_team.pokemons
        ]
        self.opponent_pokemons[0].is_active = True
        self.user_events.append(user_events.BattleReady(self.ref))

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
        self.events.append(events.HostMovePerformed(self.ref))
        self.events.append(events.OpponentMovePerformed(self.ref))
        self.events.append(events.TurnFinished(self.ref))

    def finish_turn(self):
        self.user_events.append(user_events.TurnReady(self.ref))

    def perform_move(self, pokemon: Pokemon, opponent: Pokemon):
        if pokemon.is_active:
            damage = pokemon.perform_move_against(opponent)

            user_event = user_events.PokemonUsedMove(
                self.ref,
                pokemon.pokemon.species.name,
                pokemon.next_move.name,
                damage,
            )
            self.user_events.append(user_event)

        pokemon.next_move = None

    def perform_host_move(self):
        pokemon_that_moved = next(pokemon for pokemon in self.host_pokemons if pokemon.next_move)
        self.perform_move(pokemon_that_moved, self.active_opponent_pokemon)

    def perform_opponent_move(self):
        pokemon_that_moved = next(pokemon for pokemon in self.opponent_pokemons if pokemon.next_move)
        self.perform_move(pokemon_that_moved, self.active_host_pokemon)

    def get_host_possible_moves(self):
        return [move.name for move in self.active_host_pokemon.pokemon.moves]

    def get_opponent_possible_moves(self):
        return [move.name for move in self.active_opponent_pokemon.pokemon.moves]
