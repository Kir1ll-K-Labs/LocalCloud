import asyncio
import json
import urllib.parse
from math import atan2

import aiohttp
from LocalCloud.Client.Managers.FunctionsManager.Types import FunctionResponce, FunctionInvokeError


class SenderClient:
    def __init__(self):
        pass

    @classmethod
    async def send_function(cls, address,*args,**kwargs)->FunctionResponce:
        data={
            "args":args,
            "kwargs":kwargs
        }
        headers = {
            "function_data": urllib.parse.quote(str(data), encoding="utf-8")
        }
        async with aiohttp.ClientSession() as session:
            tasks=[]

            async def send_data(address_inner:str)->FunctionResponce:
                url = f"http://{address_inner}:12123/function/get"
                async with session.get(url, timeout=3, headers=headers) as response:
                    if response.status==404:
                        raise FunctionInvokeError(message=str(await response.content.read(),encoding="utf-8"))
                    if response.status==200:
                        function_responce = FunctionResponce(status_code=200,responce=json.loads(await response.content.read()))
                        return function_responce
            return await send_data(address)