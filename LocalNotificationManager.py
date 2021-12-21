import asyncio
import desktop_notify
import desktop_notify.aio


class LocalNotificationManager:
    def __init__(self):
        self.notify_server = desktop_notify.aio.Server("notify-mirror")

    def create_local_notification(self, header, body):
        new_notification = self.notify_server.Notify(header, body)
        new_notification.set_on_close(self.on_local_notification_closed)

        # asyncio.get_event_loop().run_until_complete(new_notification.show())
        try:
            loop = asyncio.get_event_loop()
        except:
            loop = asyncio.new_event_loop()
        finally:
            loop.run_until_complete(new_notification.show())

        return new_notification

    def destroy_local_notification(self, notification):
        print("trying to destory notification")

        # asyncio.get_event_loop().run_until_complete(notification.close())
        try:
            loop = asyncio.get_event_loop()
        except:
            loop = asyncio.new_event_loop()
        finally:
            loop.run_until_complete(notification.close())

    def on_local_notification_closed(self, notification, reason):
        print(f"notification closed because: {reason}")
