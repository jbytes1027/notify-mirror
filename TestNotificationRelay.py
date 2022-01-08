import asyncio
from AndroidNotification import AndroidNotification
from AsyncRemoteNotificationRelay import AsyncRemoteNotificationRelay


class TestNotificationRelay(AsyncRemoteNotificationRelay):
    async def start(self):
        await asyncio.sleep(1)
        self._update_listeners(
            AndroidNotification("test header", "test body", "testapp", "com.test", 1)
        )
