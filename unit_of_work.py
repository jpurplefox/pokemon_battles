import abc

class AbstractUnitOfWork(abc.ABC):
    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @abc.abstractmethod
    def commit(self):
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
