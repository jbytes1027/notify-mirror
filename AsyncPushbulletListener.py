import asyncio
from asyncio.tasks import FIRST_COMPLETED
from pprint import pprint
from aiohttp.helpers import get_running_loop
import websockets
import json
import aiohttp
from AndroidNotification import AndroidNotification

from RemoteNotificationManager import RemoteNotificationListener

BASE_URL_WSS = "wss://stream.pushbullet.com/websocket/"
BASE_URL_EPHEMERALS = "https://api.pushbullet.com/v2/ephemerals"
BASE_URL_USER = "https://api.pushbullet.com/v2/users/me"


class AsyncPushbulletListener(RemoteNotificationListener):
    def __init__(self, api_key):
        super().__init__()
        self.api_key = api_key
        self.header = {
            "Access-Token": api_key,
            "Content-Type": "application/json",
        }

    def start(self):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
        finally:
            loop.run_until_complete(self._get_user())
            asyncio.run(self._receive_notification_ephemerals())

    def stop(self):
        asyncio.get_running_loop().stop()

    async def _get_user(self):
        async with aiohttp.ClientSession(headers=self.header) as session:
            async with session.get(BASE_URL_USER) as response:
                user_info = await response.json()

                print("connected to the account of " + user_info["email"])
                self.user_id = user_info["iden"]

    async def _receive_notification_ephemerals(self):
        async with websockets.connect(BASE_URL_WSS + self.api_key) as websocket:
            print("connected to websocket")
            async for message in websocket:
                message = json.loads(message)
                pprint(message)

                if message["type"] == "push":
                    self._update_listeners(
                        AndroidNotification(
                            message["title"],
                            message["body"],
                            message["application"],
                            message["package"],
                            message["id"],
                        )
                    )

    async def _send_dismissal_ephemeral(self, notification):
        print("creating dismissal ephemeral")
        ephemeral = {
            "push": {
                "notification_id": notification.id,
                "notification_tag": "",
                "package_name": notification.name,
                "source_user_iden": self.user_id,
                "type": "dismissal",
            },
            "type": "push",
        }

        async with aiohttp.ClientSession() as session:
            print("sending dismissal ephemerall")
            async with session.post(
                BASE_URL_EPHEMERALS, headers=self.header, data=json.dumps(ephemeral)
            ) as response:
                assert response.status == 200
                print("sent remote dismissal")

    def dismiss(self, notification):
        asyncio.create_task(self._send_dismissal_ephemeral(notification))
