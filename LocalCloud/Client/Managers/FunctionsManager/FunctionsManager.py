from LocalCloud.CallBackFilter import CallBackClass
from LocalCloud.Client.Managers.FunctionsManager.Types.InvokingFunction import InvokingFunction
from LocalCloud.Client.Server.Server import Server
from LocalCloud.Client.Managers.FunctionsManager.SenderClient import SenderClient

class FunctionsManager:

    class __function_class():
        def __init__(self,function,function_name):
            self.function=function
            self.function_name=function_name

        async def __call__(self, *args, **kwargs):
            return await self.function(*args,**kwargs)

        async def invoke_on_address(self,address,*args,**kwargs):
            invoking_f=InvokingFunction(address=address,function_name=self.function_name,function_data={
            "args": args,
            "kwargs": kwargs
        })
            return await SenderClient.send_function_class(invoking_f)
        def __getattr__(self, item):
            return self.function.__getattr__(item)
    def __init__(self):
        pass

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
    async def invoke(cls,invoking_function:InvokingFunction,*args,**kwargs):
        function_data = {
            "args": args,
            "kwargs": kwargs
        }
        invoking_function.function_data = function_data
        return await SenderClient.send_function_class(invoking_function)