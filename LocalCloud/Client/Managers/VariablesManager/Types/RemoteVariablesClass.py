import asyncio

from LocalCloud.Client.Managers.VariablesManager.SenderClient import SenderClient

class RemoteVariablesClass:
    def __init__(self,address):
        self.address=address
    async def get(self,*args):
        try:
            return await SenderClient.get_value(address=self.address,key=args[0])
        except KeyError as error:
            if len(args)<=1:
                raise error
            return args[1]

    async def have(self,key):
        try:
            await SenderClient.get_value(address=self.address,key=key)
            return True
        except KeyError as error:
            return False