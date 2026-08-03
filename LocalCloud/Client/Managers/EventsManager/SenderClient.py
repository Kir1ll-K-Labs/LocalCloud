import asyncio
import urllib.parse

import aiohttp

from LocalCloud.Client.Managers.EventsManager.Types import SendingEvent


class SenderClient:
    def __init__(self):
        pass

    @classmethod
    async def send_event_class(cls, event_class:SendingEvent):
        headers = {
            "event_name": urllib.parse.quote(str(event_class.event_name), encoding="utf-8"),
            "event_data": urllib.parse.quote(str(event_class.event_data), encoding="utf-8")
        }
        async with aiohttp.ClientSession() as session:
            tasks=[]

            async def send_data(address_inner:str):
                url = f"http://{address_inner}:12123/events/get"
                async with session.get(url, timeout=3, headers=headers) as response:
                    if response.status==404:
                        print(str(await response.content.read(),encoding="utf-8"))
            for address in event_class.addresses:
                tasks.append(
                    send_data(address)
                )
            await asyncio.gather(*tasks)