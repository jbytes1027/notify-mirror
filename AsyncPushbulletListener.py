import asyncio
import websockets
import json
import aiohttp
from pprint import pprint
from AndroidNotification import AndroidNotification
from RemoteNotificationManager import AsyncRemoteNotificationListener

BASE_URL_WSS = "wss://stream.pushbullet.com/websocket/"
BASE_URL_EPHEMERALS = "https://api.pushbullet.com/v2/ephemerals"
BASE_URL_USER = "https://api.pushbullet.com/v2/users/me"


class AsyncPushbulletListener(AsyncRemoteNotificationListener):
    def __init__(self, api_key):
        super().__init__()
        self.api_key = api_key
        self.header = {
            "Access-Token": api_key,
            "Content-Type": "application/json",
        }

    async def start(self):
        await self._get_user()
        asyncio.get_event_loop().create_task(self._receive_notification_ephemerals())

    # async def stop(self):
    #     asyncio.get_running_loop().stop()

    async def _get_user(self):
        async with aiohttp.ClientSession(headers=self.header) as session:
            async with session.get(BASE_URL_USER) as response:
                if response.status == 401:
                    raise Exception("Invalid Access Code")
                elif response.status == 403:
                    raise Exception("Access Denied")
                elif response.status == 429:
                    raise Exception("Too Many Requests")

                user_info = await response.json()

                print("connected to the account of " + user_info["email"])
                self.user_id = user_info["iden"]

    async def _receive_notification_ephemerals(self):
        async with websockets.connect(BASE_URL_WSS + self.api_key) as websocket:
            print("connected to websocket")
            async for message in websocket:
                message = json.loads(message)
                pprint(message)

                if message["type"] == "push" and message["push"]["type"] == "mirror":
                    self._update_listeners(
                        AndroidNotification(
                            message["push"]["title"],
                            message["push"]["body"],
                            message["push"]["application_name"],
                            message["push"]["package_name"],
                            message["push"]["notification_id"],
                        )
                    )

    # async def _send_dismissal_ephemeral(self, notification):
    #     print("creating dismissal ephemeral")
    #     ephemeral = {
    #         "push": {
    #             "notification_id": notification.id,
    #             "notification_tag": "",
    #             "package_name": notification.name,
    #             "source_user_iden": self.user_id,
    #             "type": "dismissal",
    #         },
    #         "type": "push",
    #     }

    #     async with aiohttp.ClientSession() as session:
    #         print("sending dismissal ephemerall")
    #         async with session.post(
    #             BASE_URL_EPHEMERALS, headers=self.header, data=json.dumps(ephemeral)
    #         ) as response:
    #             assert response.status == 200
    #         print("sent remote dismissal")

    def dismiss(self, notification):
        asyncio.create_task(self._send_dismissal_ephemeral(notification))
