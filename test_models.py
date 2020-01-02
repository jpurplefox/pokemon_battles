import models

def test_pokemon_calculates_stats_properly():
    spark = models.Pokemon('Spark', models.known_species['pikachu'], level=20)

    assert spark.max_hp == 44
    assert spark.attack == 27
    assert spark.defense == 17
    assert spark.sp_attack == 25
    assert spark.sp_defense == 21
    assert spark.speed == 41

def test_pokemon_initializes_healthy():
    spark = models.Pokemon('Spark', models.known_species['pikachu'], level=20)

    assert spark.hp == spark.max_hp

def test_pokemon_receives_damage_and_looses_hp():
    spark = models.Pokemon('Spark', models.known_species['pikachu'], level=10)

    spark.receive_damage(10)

    assert spark.max_hp == 27
    assert spark.hp == 17

def test_pokemon_attacks_other_pokemon_and_makes_damage():
    thunder_shock = models.known_moves['thunder shock']
    spark = models.Pokemon(
        'Spark',
        models.known_species['pikachu'],
        level=10,
        moves=[thunder_shock]
    )
    bubble = models.Pokemon('Bubble', models.known_species['squirtle'], level=10)

    damage = spark.perform_move_against(thunder_shock, bubble)

    assert damage == 6
    assert bubble.hp == 22

def test_can_add_a_pokemon_to_a_team():
    spark = models.Pokemon('Spark', models.known_species['pikachu'], level=10)
    team = models.Team('My team')
    team.add_pokemon(spark)

    assert spark in team.pokemons
