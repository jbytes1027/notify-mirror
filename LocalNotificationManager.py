import asyncio
import desktop_notify


class LocalNotificationManager:
    def __init__(self):
        self.notify_server = desktop_notify.aio.Server("notify-mirror")

    def _destroy(self, notification):
        print("trying to destory notification")

        asyncio.get_event_loop().run_until_complete(notification.close())

    def on_local_closed(self, notification, reason):
        print(f"notification closed because: {reason}")

    def on_new(self, android_notification):
        print("new notification received")
        local_notification = self.notify_server.Notify(
            android_notification.header, android_notification.body
        )
        local_notification.set_on_close(self.on_local_closed)

        asyncio.get_event_loop().create_task(local_notification.show())
