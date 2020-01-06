import abc

from . import messagebus


class AbstractUnitOfWork(abc.ABC):
    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    def commit(self):
        self._commit()
        self.publish_events()

    def publish_events(self):
        for battle in self.battles.seen:
            while battle.events:
                event = battle.events.pop(0)
                messagebus.handle(event, uow=self)

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
