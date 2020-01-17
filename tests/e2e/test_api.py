import requests

from pokemon_battles import config
from ..random_refs import random_team_name


def post_to_add_team(name):
    url = config.get_api_url()
    r = requests.post(
        f'{url}/add_team',
        json={'name': name}
    )
    assert r.status_code == 201


def post_to_add_pokemon_to_team(team_name, nickname, species, level, moves):
    url = config.get_api_url()
    r = requests.post(
        f'{url}/add_pokemon',
        json={
            'team_name': team_name,
            'nickname': nickname,
            'species': species,
            'level': level,
            'moves': moves,
        }
    )
    assert r.status_code == 200


def post_to_host_a_battle(team_name):
    url = config.get_api_url()
    r = requests.post(
        f'{url}/host_battle',
        json={'team_name': team_name}
    )
    data = r.json()
    assert r.status_code == 201
    assert 'battle_ref' in data

    return data['battle_ref']


def post_to_join_a_battle(battle_ref, team_name):
    url = config.get_api_url()
    r = requests.post(
        f'{url}/join_battle',
        json={'battle_ref': battle_ref, 'team_name': team_name}
    )
    assert r.status_code == 200


def post_to_register_a_move(battle_ref, player, move_name):
    url = config.get_api_url()
    r = requests.post(
        f'{url}/register_a_move',
        json={'battle_ref': battle_ref, 'player': player, 'move_name': move_name}
    )
    assert r.status_code == 200
    

def test_team_creation_happy_path():
    team_name = random_team_name()
    post_to_add_team(team_name)

    post_to_add_pokemon_to_team(team_name, 'Spark', 'Pikachu', 20, ['Thunder Shock'])

def test_battle_happy_path():
    host_team_name, opponent_team_name = random_team_name(), random_team_name()

    post_to_add_team(host_team_name)
    post_to_add_pokemon_to_team(host_team_name, 'Spark', 'Pikachu', 20, ['Thunder Shock'])

    post_to_add_team(opponent_team_name)
    post_to_add_pokemon_to_team(opponent_team_name, 'Bubble', 'Squirtle', 20, ['Bubble'])

    battle_ref = post_to_host_a_battle(host_team_name)
    post_to_join_a_battle(battle_ref, opponent_team_name)

    post_to_register_a_move(battle_ref, 'host', 'Thunder Shock')
    post_to_register_a_move(battle_ref, 'opponent', 'Bubble')
