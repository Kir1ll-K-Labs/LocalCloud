import asyncio
import json
import urllib.parse

import aiohttp
from LocalCloud.Client.Managers.FunctionsManager.Types import InvokingFunction, FunctionInvokeError


class SenderClient:
    def __init__(self):
        pass

    @classmethod
    async def send_function_class(cls, function_class:InvokingFunction):
        headers = {
            "function_name": urllib.parse.quote(str(function_class.function_name), encoding="utf-8"),
            "function_data": urllib.parse.quote(str(function_class.function_data), encoding="utf-8")
        }
        async with aiohttp.ClientSession() as session:
            tasks=[]

            async def send_data(address_inner:str):
                url = f"http://{address_inner}:12123/function/get"
                async with session.get(url, timeout=3, headers=headers) as response:
                    if response.status==404:
                        raise FunctionInvokeError(message=str(await response.content.read(),encoding="utf-8"))
                    if response.status==200:
                        return json.loads(await response.content.read())
            return await send_data(function_class.address)