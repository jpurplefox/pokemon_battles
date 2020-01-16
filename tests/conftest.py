import pytest
from pymongo import MongoClient

from pokemon_battles import config


@pytest.fixture
def mongo_database():
    client = MongoClient(config.get_mongo_uri())
    return client.test_database
