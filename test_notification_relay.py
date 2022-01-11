import asyncio
from android_notification import AndroidNotification
from async_remote_notification_relay import AsyncRemoteNotificationRelay


class TestNotificationRelay(AsyncRemoteNotificationRelay):
    async def start(self):
        await asyncio.sleep(1)
        self._update_listeners(
            AndroidNotification("test header", "test body", "testapp", "com.test", 1)
        )
