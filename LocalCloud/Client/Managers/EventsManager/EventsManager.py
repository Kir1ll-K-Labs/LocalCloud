from LocalCloud.CallBackFilter import CallBackClass
from LocalCloud.Client.Managers.EventsManager.SenderClient import SenderClient
from LocalCloud.Client.Server import Server
from LocalCloud.CallBackFilter.Handlers import Handlers
class EventsManager:

    class __event_class():
        def __init__(self,function,event_name:str=""):
            self.function=function
            self.event_name=event_name

        async def __call__(self, *args, **kwargs):
            return await self.function(*args,**kwargs)

        async def send_to_addresses(self,addresses,*args,**kwargs):
            await EventsManager.send_event(
                addresses=addresses,*args,**kwargs
            )
        def __getattr__(self, item):
            return self.function.__getattr__(item)
    def __init__(self):
        pass

    @classmethod
    def init(cls):
        Server.init()
        Server._start_server()

    @classmethod
    def get_handlers(cls)->Handlers:
        return Handlers(handlers_list=Server._on_event_receive_callbacks)
    @classmethod
    def echo_event(cls,**kwargs):
        def decorator(function):
            if "event_name" in kwargs:
                kwargs["event_name"]=kwargs["event_name"]
            event_class=cls.__event_class(function=function,event_name=kwargs.get("event_name",""))
            call_back_class=CallBackClass(function=function,kwargs=kwargs)
            if not hasattr(Server,"_on_event_receive_callbacks"):
                Server._on_event_receive_callbacks=[]
            Server._on_event_receive_callbacks.append(call_back_class)
            return event_class
        return decorator

    @classmethod
    async def send_event(cls,_addresses_,*args,**kwargs):
        event_data={
            "args":args,
            "kwargs":kwargs
        }
        await SenderClient.send_event(_addresses_,event_data)