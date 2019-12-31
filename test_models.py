import models

def test_pokemon_receives_damage_and_looses_hp():
    pikachu = models.Pokemon(
        'Pikachu',
        hp=35,
        attack=55,
        defense=30,
    )

    pikachu.receive_damage(10)

    assert pikachu.hp == 25

def test_pokemon_attacks_other_pokemon_and_makes_damage():
    thunder_shock = models.Move('Thunder Shock', 40)
    pikachu = models.Pokemon(
        'Pikachu',
        hp=35,
        attack=55,
        defense=30,
        moves=[thunder_shock],
    )
    squirtle = models.Pokemon('Squirtle', hp=44, attack=48, defense=65)

    damage = pikachu.perform_move_against(thunder_shock, squirtle)

    assert damage == 35
    assert squirtle.hp == 9
