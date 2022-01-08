import asyncio
import desktop_notify


class LocalNotificationManager:
    def __init__(self):
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
        print(f"notification closed because: {closed_reasons[reason]}")

    def on_new(self, android_notification):
        print("new notification received")

        local_notification = self.notify_server.Notify(
            android_notification.header, android_notification.body
        )
        local_notification.set_on_close(self.on_local_closed)

        asyncio.get_event_loop().create_task(local_notification.show())


#         new_notification.add_action(
#             "default", "_", on_local_notification_user_clicked, None
#         )
#         new_notification.connect("closed", on_local_notification_user_closed)


#         # apply config settings
#         timeout_setting = config_manager.get_ephemeral_setting(ephemeral, "timeout")
#         if timeout_setting != "default":
#             new_notification.set_timeout(timeout_setting)

#         urgency_setting = config_manager.get_ephemeral_setting(ephemeral, "urgency")
#         if urgency_setting != "default":
#             new_notification.set_urgency(urgency_setting)
