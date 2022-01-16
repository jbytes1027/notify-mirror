#!/usr/bin/env python3

import asyncio
import asyncio_glib
from async_pushbullet_relay import AsyncPushbulletRelay
from test_notification_relay import TestNotificationRelay

from config_manager import ConfigManager
import os

from local_notification_manager import LocalNotificationManager


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--config",
        type=str,
        help="config file path",
        default=ConfigManager.DEFAULT_CONFIG_PATH,
    )
    args = parser.parse_args()

    # setup event loop
    asyncio.set_event_loop_policy(asyncio_glib.GLibEventLoopPolicy())

    config_manager = ConfigManager(args.config)
    remote_relay = AsyncPushbulletRelay(config_manager.get_api_key())
    # remote_relay = TestNotificationRelay()

    local_notification_manager = LocalNotificationManager(config_manager)
    remote_relay.add_listener(local_notification_manager)

    event_loop = asyncio.new_event_loop()
    event_loop.create_task(remote_relay.start())

    try:
        print("started pb")
        event_loop.run_forever()
    except KeyboardInterrupt:
        print("program closed")


if __name__ == "__main__":
    main()
