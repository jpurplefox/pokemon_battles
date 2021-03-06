from dataclasses import dataclass, field


class Command:
    pass


@dataclass(frozen=True)
class AddTeam(Command):
    name: str


@dataclass(frozen=True)
class AddPokemonToTeam(Command):
    team_name: str
    nickname: str
    species: str
    lvl: int
    move_names: list = field(default_factory=list)


@dataclass(frozen=True)
class HostBattle(Command):
    team_name: str


@dataclass(frozen=True)
class JoinBattle(Command):
    battle_ref: str
    team_name: str


@dataclass(frozen=True)
class RegisterUseMove(Command):
    battle_ref: str
    player: str
    move_name: str


@dataclass(frozen=True)
class RegisterChangePokemon(Command):
    battle_ref: str
    player: str
    pokemon_nickname: str
