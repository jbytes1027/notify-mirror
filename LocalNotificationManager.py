import asyncio
import desktop_notify


class LocalNotificationManager:
    def __init__(self, config_manager):
        self.active_notifications = []
        self.notify_server = desktop_notify.aio.Server("notify-mirror")

    def _destroy(self, notification):
        print("trying to destory notification")

        asyncio.get_event_loop().run_until_complete(notification.close())

    def on_local_closed(self, notification, reason):
        closed_reasons = {
            1: "EXPIRED",
            2: "DISMISSED",
            3: "CLOSED BY PROGRAM",
            4: "UNDEFINED",
        }
        print(notification)
        print(f"notification closed because: {closed_reasons[reason]}")

    def on_new(self, android_notification):
        print("new notification received")

        local_notification = self.notify_server.Notify(
            android_notification.header, android_notification.body
        )
        local_notification.set_on_close(self.on_local_closed)

        # apply config settings
        timeout_setting = self.config_manager.get_notification_setting(
            android_notification, self.config_manager.SETTING_NOTIFICATION_TIMEOUT
        )
        if timeout_setting != "default":
            local_notification.set_timeout(int(timeout_setting))

        # show notification
        asyncio.get_event_loop().create_task(local_notification.show())


#         new_notification.add_action(
#             "default", "_", on_local_notification_user_clicked, None
#         )
#         new_notification.connect("closed", on_local_notification_user_closed)
