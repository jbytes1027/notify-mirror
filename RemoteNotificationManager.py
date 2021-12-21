from abc import abstractmethod


class RemoteNotificationListener:
    def __init__(self):
        self._listeners = []

    @abstractmethod
    def start(self):
        raise NotImplementedError()

    @abstractmethod
    def stop(self):
        raise NotImplementedError()

    @abstractmethod
    def dismiss(self, notification):
        raise NotImplementedError()

    def _update_listeners(self, notification):
        for listener in self._listeners:
            listener.update(notification)

    def add_listener(self, listener):
        self._listeners.append(listener)
