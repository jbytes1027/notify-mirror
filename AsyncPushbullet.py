from pprint import pprint
import websockets
import json
import aiohttp

BASE_URL_WSS = "wss://stream.pushbullet.com/websocket/"
BASE_URL_EPHEMERALS = "https://api.pushbullet.com/v2/ephemerals"


class AsyncPushbulletManager:
    def __init__(self, api_key):
        self.api_key = api_key
        self.header = {
            "Access-Token": api_key,
            "Content-Type": "application/json",
        }

    async def receive_notification_ephemerals(self, message_handler):
        async with websockets.connect(BASE_URL_WSS + self.api_key) as websocket:
            print("connected to websocket")
            async for message in websocket:
                message = json.loads(message)
                pprint(message)

                if message["type"] == "push":
                    message_handler(message["push"])

            # print(await websocket.recv())

    async def send_dismissal_ephemeral(
        self, notification_id, notification_tag, package_name, user_id
    ):
        print("creating dismissal ephemeral")
        ephemeral = {
            "push": {
                "notification_id": notification_id,
                "notification_tag": notification_tag,
                "package_name": package_name,
                "source_user_iden": user_id,
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