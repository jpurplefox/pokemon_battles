import pytest

import models

@pytest.fixture
def pikachu():
    return models.Species(
        'Pikachu',
        hp=35,
        attack=55,
        defense=30,
        sp_attack=50,
        sp_defense=40,
        speed=90,
    )

@pytest.fixture
def squirtle():
    return models.Species(
        'Squirtle',
        hp=44,
        attack=48,
        defense=65,
        sp_attack=50,
        sp_defense=64,
        speed=43,
    )

def test_pokemon_calculates_stats_properly(pikachu):
    spark = models.Pokemon(
        'Spark',
        pikachu,
        level=20,
    )

    assert spark.max_hp == 44
    assert spark.attack == 27
    assert spark.defense == 17
    assert spark.sp_attack == 25
    assert spark.sp_defense == 21
    assert spark.speed == 41

def test_pokemon_initializes_healthy(pikachu):
    spark = models.Pokemon(
        'Spark',
        pikachu,
        level=20,
    )

    assert spark.hp == spark.max_hp

def test_pokemon_receives_damage_and_looses_hp(pikachu):
    spark = models.Pokemon(
        'Spark',
        pikachu,
        level=10,
    )

    spark.receive_damage(10)

    assert spark.max_hp == 27
    assert spark.hp == 17

def test_pokemon_attacks_other_pokemon_and_makes_damage(pikachu, squirtle):
    thunder_shock = models.Move('Thunder Shock', 40)

    spark = models.Pokemon('Spark', pikachu, level=10, moves=[thunder_shock])
    bubble = models.Pokemon('Bubble', squirtle, level=10)

    damage = spark.perform_move_against(thunder_shock, bubble)

    assert damage == 6
    assert bubble.hp == 22
