#!/usr/bin/env python3

import asyncio
from pprint import pprint
import asyncio_glib
from AsyncPushbulletRelay import AsyncPushbulletRelay
from TestNotificationRelay import TestNotificationRelay

from ConfigManager import ConfigManager
from os import popen

from LocalNotificationManager import LocalNotificationManager

# def on_local_notification_user_clicked(notification, event, _):
#     print("notification clicked")
#     command = config_manager.get_ephemeral_setting(
#         active_mirrored_notifications[notification]
#     )
#     if command == "":
#         return
#     else:
#         popen(command)


def main():
    asyncio.set_event_loop_policy(asyncio_glib.GLibEventLoopPolicy())

    config_manager = ConfigManager()
    # remote_relay = AsyncPushbulletRelay(config_manager.get_api_key())
    remote_relay = TestNotificationRelay()

    local_notification_manager = LocalNotificationManager()
    remote_relay.add_listener(local_notification_manager)

    event_loop = asyncio.new_event_loop()
    event_loop.create_task(remote_relay.start())

    try:
        print("started pb")
        event_loop.run_forever()
    except KeyboardInterrupt:
        print("program closed")

    # asyncio.run(
    #     pushbullet_manager.receive_notification_ephemerals(
    #         on_new_notification_ephemeral
    #     )
    # )


if __name__ == "__main__":
    main()
