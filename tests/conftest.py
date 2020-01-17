import pytest
from pymongo import MongoClient
from redis import Redis

from pokemon_battles import config


@pytest.fixture
def mongo_database():
    client = MongoClient(config.get_mongo_uri())
    return client.test_database


@pytest.fixture
def redis_client():
    return Redis.from_url(url=config.get_redis_uri())
