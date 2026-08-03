from LocalCloud.CallBackFilter import CallBackClass
from LocalCloud.Client.Managers.EventsManager.SenderClient import SenderClient
from LocalCloud.Client.Managers.EventsManager.Types import SendingEvent
from LocalCloud.Client.Server import Server
class EventsManager:

    class __event_class():
        def __init__(self,function,event_name:str=""):
            self.function=function
            self.event_name=event_name

        async def __call__(self, *args, **kwargs):
            return await self.function(*args,**kwargs)

        async def send_to_addresses(self,addresses,*args,**kwargs):
            await EventsManager.send_event(
                SendingEvent(
                    addresses=addresses,
                    event_name=self.event_name
                ),*args,**kwargs
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
    async def send_event(cls,sending_event:SendingEvent,*args,**kwargs):
        event_data={
            "args":args,
            "kwargs":kwargs
        }
        sending_event.event_data=event_data
        await SenderClient.send_event_class(sending_event)