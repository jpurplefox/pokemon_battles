from pokemon_battles.domain import models

def test_pokemon_calculates_stats_properly():
    spark = models.Pokemon('Spark', models.known_species['Pikachu'], level=20)

    assert spark.max_hp == 44
    assert spark.attack == 27
    assert spark.defense == 17
    assert spark.sp_attack == 25
    assert spark.sp_defense == 21
    assert spark.speed == 41
