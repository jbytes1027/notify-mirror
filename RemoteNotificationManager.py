from abc import abstractmethod


class AsyncRemoteNotificationListener:
    def __init__(self):
        self._listeners = []

    @abstractmethod
    async def start(self):
        raise NotImplementedError()

    @abstractmethod
    async def stop(self):
        raise NotImplementedError()

    @abstractmethod
    def dismiss(self, notification):
        raise NotImplementedError()

    def _update_listeners(self, android_notification):
        print("updating listeners")
        for listener in self._listeners:
            listener.on_new(android_notification)

    def add_listener(self, listener):
        self._listeners.append(listener)
