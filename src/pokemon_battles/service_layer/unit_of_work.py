import abc
from pymongo import MongoClient
from redis import Redis

from pokemon_battles import config
from pokemon_battles.adapters import repositories
from . import messagebus


class AbstractUnitOfWork(abc.ABC):
    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    def commit(self):
        self._commit()
        self.publish_events()
        self.publish_user_events()

    def publish_events(self):
        for battle in self.battles.seen:
            while battle.events:
                event = battle.events.pop(0)
                messagebus.handle(event, uow=self)

    def publish_user_events(self):
        for battle in self.battles.seen:
            while battle.user_events:
                event = battle.user_events.pop(0)
                self.user_messagebus.emit(event)

    @abc.abstractmethod
    def _commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError

    def init_repositories(self, team_repository, battle_repository):
        self._teams = team_repository
        self._battles = battle_repository

    @property
    def teams(self):
        return self._teams

    @property
    def battles(self):
        return self._battles


class UnitOfWork(AbstractUnitOfWork):
    def __init__(self):
        mongo_database = MongoClient(config.get_mongo_uri()).pokemon
        redis_client = Redis.from_url(url=config.get_redis_uri())
        self.init_repositories(
            repositories.MongoTeamRepository(mongo_database),
            repositories.RedisBattleRepository(redis_client)
        )

    def _commit(self):
        for team in self._teams.seen:
            self._teams.update(team)

    def rollback(self):
        pass
