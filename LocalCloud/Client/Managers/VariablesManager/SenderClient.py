import asyncio
import json
import urllib.parse

import aiohttp
from LocalCloud.Client.Managers.FunctionsManager.Types import InvokingFunction


class SenderClient:
    def __init__(self):
        pass
    @classmethod
    async def get_value(cls,address:str,key):
        headers = {
            "key": urllib.parse.quote(str(key), encoding="utf-8")
        }
        async with aiohttp.ClientSession() as session:
            url = f"http://{address}:12123/variables/get"
            async with session.get(url, timeout=3, headers=headers) as response:
                if response.status == 404:
                    raise KeyError(f"Key: {key} not found in {address}")
                if response.status == 200:
                    return json.loads(await response.content.read())