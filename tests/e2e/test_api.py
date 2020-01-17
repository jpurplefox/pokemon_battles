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

def post_to_add_pokemon_to_a_team(team_name, nickname, species, level, moves):
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
    

def test_team_creation_returns_201():
    team_name = random_team_name()
    post_to_add_team(team_name)

    post_to_add_pokemon_to_a_team(team_name, 'Spark', 'Pikachu', 20, ['Thunder Shock'])
