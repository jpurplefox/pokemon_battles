import abc

import user_events


class AbstractUserMessagebus(abc.ABC):
    pass

    @abc.abstractmethod
    def emit(self, event: user_events.UserEvent):
        raise NotImplementedError
