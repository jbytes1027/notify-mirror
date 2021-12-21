from abc import abstractmethod


class RemoteNotificationClient:
    def __init__(self):
        self._listeners = []

    @abstractmethod
    def dismiss(self, notification):
        raise NotImplementedError()

    def _update_listeners(self, notification):
        for listener in self._listeners:
            listener.update(notification)

    def add_listener(self, listener):
        self._listeners.append(listener)
