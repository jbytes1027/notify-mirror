#!/usr/bin/env python3

import asyncio
from pprint import pprint
import asyncio_glib
from AsyncPushbulletClient import AsyncPushbulletClient

from ConfigManager import ConfigManager
from os import popen

import base64
from gi.repository import Notify
from gi.repository import GdkPixbuf

active_mirrored_notifications = {}
pushbullet_manager = None
config_manager = None


def get_pixbuf_from_ephemeral(ephemeral):
    raw_data = base64.b64decode(ephemeral["icon"])
    return GdkPixbuf.Pixbuf.new_from_data(
        raw_data,
        GdkPixbuf.Colorspace(0),
        True,
    )


def get_notification_from_ephemeral(ephemeral):
    for n, pbn in active_mirrored_notifications.items():
        if (
            pbn["notification_id"] == ephemeral["notification_id"]
            and pbn["package_name"] == ephemeral["package_name"]
        ):
            return n


def on_local_notification_user_clicked(notification, event, _):
    print("notification clicked")
    command = config_manager.get_ephemeral_setting(
        active_mirrored_notifications[notification]
    )
    if command == "":
        return
    else:
        popen(command)


def on_local_notification_user_closed(notification):
    closed_reasons = {
        1: "EXPIRED",
        2: "DISMISSED",
        3: "CLOSED BY PROGRAM",
        4: "UNDEFINED",
    }
    print(
        f"notification closed because: {closed_reasons[notification.get_closed_reason()]}"
    )

    if notification in active_mirrored_notifications.keys():
        ephemeral = active_mirrored_notifications[notification]

        if "notification_tag" in ephemeral.keys():
            n_tag = ephemeral["notification_tag"]
        else:
            n_tag = None

        asyncio.create_task(
            pushbullet_manager.send_dismissal_ephemeral(
                ephemeral["notification_id"],
                n_tag,
                ephemeral["package_name"],
                ephemeral["source_user_iden"],
            )
        )
    else:
        print("notification dismissed by remote")


def on_new_notification_ephemeral(ephemeral):
    print(f"new {ephemeral['type']} ephemeral")

    # update local info if existing
    # if found in local notification then close and remove from local
    if ephemeral["type"] == "dismissal":
        found_notification = get_notification_from_ephemeral(ephemeral)
        if found_notification != None:
            found_notification.close()
            active_mirrored_notifications.pop(found_notification)

    if ephemeral["type"] == "mirror" and ephemeral["dismissible"]:
        # create local notificaion
        new_notification = Notify.Notification.new(
            ephemeral["title"], ephemeral["body"]
        )

        # apply config settings
        timeout_setting = config_manager.get_ephemeral_setting(ephemeral, "timeout")
        if timeout_setting != "default":
            new_notification.set_timeout(timeout_setting)

        urgency_setting = config_manager.get_ephemeral_setting(ephemeral, "urgency")
        if urgency_setting != "default":
            new_notification.set_urgency(urgency_setting)

        # new_notification.set_image_from_pixbuf(get_pixbuf_from_ephemeral(pb_ephemeral))

        # connect callbacks
        new_notification.add_action(
            "default", "_", on_local_notification_user_clicked, None
        )
        new_notification.connect("closed", on_local_notification_user_closed)

        new_notification.show()
        active_mirrored_notifications[new_notification] = ephemeral


def main():
    asyncio.set_event_loop_policy(asyncio_glib.GLibEventLoopPolicy())

    config_manager = ConfigManager()

    # if not Notify.init("notify-mirror"):
    # print("error starting libnotify")

    pushbullet_manager = AsyncPushbulletClient(config_manager.get_api_key())
    # asyncio.run(
    #     pushbullet_manager.receive_notification_ephemerals(
    #         on_new_notification_ephemeral
    #     )
    # )


if __name__ == "__main__":
    main()
