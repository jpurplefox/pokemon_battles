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
    'Caterpie': Species(
        'Caterpie',
        hp=45,
        attack=30,
        defense=35,
        sp_attack=20,
        sp_defense=20,
        speed=45,
    ),
    'Ninetales': Species(
        'Ninetales',
        hp=73,
        attack=76,
        defense=75,
        sp_attack=81,
        sp_defense=100,
        speed=100,
    ),
}


@dataclass(frozen=True)
class Move:
    name: str
    power: int


known_moves = {
    'Thunder Shock': Move('Thunder Shock', 40),
    'Bubble': Move('Bubble', 40),
    'Flamethrower': Move('Flamethrower', 90),
    'Tackle': Move('Tackle', 40),
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

    def to_dict(self):
        return {
            'pokemon': self.pokemon.to_dict(),
            'hp': self.hp,
            'is_active': self.is_active,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            pokemon=Pokemon.from_dict(data['pokemon']),
            hp=data['hp'],
            is_active=data['is_active'],
        )

    def receive_damage(self, damage):
        self.hp = self.hp - damage

    def perform_move_against(self, move, other_pokemon):
        level_factor = 2 + 2 * self.pokemon.level / 5
        attack_defense_ratio = self.pokemon.attack / other_pokemon.pokemon.defense
        damage = math.floor(level_factor * move.power * attack_defense_ratio / 50) + 2
        other_pokemon.receive_damage(damage)

        return damage

    @property
    def is_fainted(self):
        return self.hp <= 0

    def set_active(self, value):
        self.is_active = value


class Action:
    @staticmethod
    def from_dict(data):
        if not data:
            return None
        return actions[data['action_type']].from_dict(data['action_data'])


@dataclass
class ActionChangePokemon(Action):
    pokemon_nickname: str

    def to_dict(self):
        return {
            'action_type': 'change_pokemon',
            'action_data': {'pokemon_nickname': self.pokemon_nickname}
        }

    @classmethod
    def from_dict(cls, data):
        return cls(pokemon_nickname=data['pokemon_nickname'])


@dataclass
class ActionUseMove(Action):
    pokemon_nickname: str
    move: str

    def to_dict(self):
        return {
            'action_type': 'use_move',
            'action_data': {'pokemon_nickname': self.pokemon_nickname, 'move': self.move}
        }

    @classmethod
    def from_dict(cls, data):
        return cls(pokemon_nickname=data['pokemon_nickname'], move=data['move'])


actions = {
    'change_pokemon': ActionChangePokemon,
    'use_move': ActionUseMove,
}


@dataclass
class Battle:
    ref: str
    host_pokemons: List[BattlingPokemon]
    opponent_pokemons: List[BattlingPokemon] = field(default_factory=list)
    host_action: Action = None
    opponent_action: Action = None

    events: list = field(default_factory=list, repr=False, compare=False)
    user_events: list = field(default_factory=list, repr=False, compare=False)

    def to_dict(self):
        return {
            'ref': self.ref,
            'host_pokemons': [pokemon.to_dict() for pokemon in self.host_pokemons],
            'opponent_pokemons': [pokemon.to_dict() for pokemon in self.opponent_pokemons],
            'host_action': self.host_action.to_dict() if self.host_action else None,
            'opponent_action': self.opponent_action.to_dict() if self.opponent_action else None,
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
            host_action=Action.from_dict(data.get('host_action')),
            opponent_action=Action.from_dict(data.get('opponent_action')),
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

    def register_use_move(self, player: str, move_name: str):
        if player == 'host':
            self.host_action = ActionUseMove(self.active_host_pokemon.pokemon.nickname, move_name)
        if player == 'opponent':
            self.opponent_action = ActionUseMove(self.active_opponent_pokemon.pokemon.nickname, move_name)

        if self.host_action and self.opponent_action:
            self.events.append(events.TurnReady(self.ref))

    def register_change_pokemon(self, player: str, pokemon_nickname: str):
        if player == 'host':
            self.host_action = ActionChangePokemon(pokemon_nickname)
        if player == 'opponent':
            self.opponent_action = ActionChangePokemon(pokemon_nickname)

        if self.host_action and self.opponent_action:
            self.events.append(events.TurnReady(self.ref))

    def change_pokemon(self, player: str, pokemon_nickname: str):
        if player == 'host':
            pokemons = self.host_pokemons
        if player == 'opponent':
            pokemons = self.opponent_pokemons
        [pokemon.set_active(False) for pokemon in pokemons]
        [pokemon.set_active(True) for pokemon in pokemons if pokemon.pokemon.nickname == pokemon_nickname]
        print(pokemon_nickname)
        print(self.active_opponent_pokemon)
        self.user_events.append(user_events.PokemonChanged(self.ref, player, pokemon_nickname))

    def process_turn(self):
        if isinstance(self.host_action, ActionUseMove):
            self.events.append(events.MovePerformed(
                self.ref,
                'host',
                self.active_host_pokemon.pokemon.nickname,
                self.host_action.move,
            ))
        if isinstance(self.host_action, ActionChangePokemon):
            self.events.append(
                events.PokemonChanged(self.ref, 'host', self.host_action.pokemon_nickname)
            )

        if isinstance(self.opponent_action, ActionUseMove):
            self.events.append(events.MovePerformed(
                self.ref,
                'opponent',
                self.active_opponent_pokemon.pokemon.nickname,
                self.opponent_action.move,
            ))
        if isinstance(self.opponent_action, ActionChangePokemon):
            self.events.append(
                events.PokemonChanged(self.ref, 'opponent', self.opponent_action.pokemon_nickname)
            )

        self.host_action = None
        self.opponent_action = None

        self.events.append(events.TurnFinished(self.ref))

    def finish_turn(self):
        if self.active_host_pokemon.is_fainted:
            self.user_events.append(
                user_events.PokemonFainted(self.ref, self.active_host_pokemon.pokemon.species.name)
            )
            self.user_events.append(user_events.BattleFinished(self.ref, 'opponent'))
        elif self.active_opponent_pokemon.is_fainted:
            self.user_events.append(
                user_events.PokemonFainted(self.ref, self.active_opponent_pokemon.pokemon.species.name)
            )
            self.user_events.append(user_events.BattleFinished(self.ref, 'host'))
        else:
            self.user_events.append(user_events.TurnReady(self.ref))

    def _perform_move(self, pokemon: Pokemon, move: Move, opponent: Pokemon):
        if pokemon.is_active:
            damage = pokemon.perform_move_against(move, opponent)

            user_event = user_events.PokemonUsedMove(
                self.ref,
                pokemon.pokemon.species.name,
                move.name,
                damage,
            )
            self.user_events.append(user_event)

        pokemon.next_move = None

    def perform_move(self, player: str, pokemon_nickname: str, move_name):
        if player == 'host':
            pokemon_that_moved = self.active_host_pokemon
            pokemon_that_receive_move = self.active_opponent_pokemon
        if player == 'opponent':
            pokemon_that_moved = self.active_opponent_pokemon
            pokemon_that_receive_move = self.active_host_pokemon
        move = known_moves[move_name]
        self._perform_move(pokemon_that_moved, move, pokemon_that_receive_move)

    def get_possible_moves(self, player):
        if player == 'host':
            moves = self.active_host_pokemon.pokemon.moves
        if player == 'opponent':
            moves = self.active_opponent_pokemon.pokemon.moves
        return [move.name for move in moves]

    def get_inactive_pokemons(self, player):
        if player == 'host':
            pokemons = self.host_pokemons
        if player == 'opponent':
            pokemons = self.opponent_pokemons
        return [pokemon.pokemon.nickname for pokemon in pokemons if not pokemon.is_active]
