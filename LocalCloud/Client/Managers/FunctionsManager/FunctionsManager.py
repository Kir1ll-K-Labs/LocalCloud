from LocalCloud.CallBackFilter.Handlers import Handlers
from LocalCloud.Client.Server import Server
from LocalCloud.CallBackFilter import CallBackClass
from LocalCloud.Client.Managers.FunctionsManager.Types.FunctionResponce import FunctionResponce
from LocalCloud.Client.Managers.FunctionsManager.SenderClient import SenderClient

class FunctionsManager:

    class __function_class():
        def __init__(self,function,function_name):
            self.function=function
            self.function_name=function_name

        async def __call__(self, *args, **kwargs):
            return await self.function(*args,**kwargs)

        async def invoke_on_address(self,address,*args,**kwargs):
            return await SenderClient.send_function(address=address,*args,**kwargs)
        def __getattr__(self, item):
            return self.function.__getattr__(item)
    def __init__(self):
        pass

    @classmethod
    def get_handlers(cls) -> Handlers:
        return Handlers(handlers_list=Server._on_function_receive_callbacks)

    @classmethod
    def init(cls):
        Server.init()
        Server._start_server()

    @classmethod
    def on_invoke(cls, **kwargs):
        def decorator(function)->cls.__function_class:
            if not "function_name" in kwargs:
                kwargs["function_name"]=function.__name__
            function_class=cls.__function_class(function=function,function_name=kwargs["function_name"])
            call_back_class = CallBackClass(function=function, kwargs=kwargs)
            if not hasattr(Server, "_on_function_receive_callbacks"):
                Server._on_function_receive_callbacks = []
            Server._on_function_receive_callbacks.append(call_back_class)
            return function_class

        return decorator
    @classmethod
    async def invoke(cls,_address_,*args,**kwargs)->FunctionResponce:
        return await SenderClient.send_function(_address_,*args,**kwargs)