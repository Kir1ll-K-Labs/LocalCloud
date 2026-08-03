import asyncio

from .CallBackClass import CallBackClass

class CallBackFilter:
    def __init__(self):
        pass

    @classmethod
    async def get_available_callbacks(cls,callbacks_list:[CallBackClass],object):

        c_weight=-1
        c_list_of_callbacks=[]
        for callback_class in callbacks_list:
            callback_class:CallBackClass
            weight=await callback_class.get_weight(object=object)
            if weight==-1:
                continue
            if weight>c_weight:
                c_list_of_callbacks=[callback_class]
                c_weight=weight
            elif weight==c_weight:
                c_list_of_callbacks.append(callback_class)
        return c_list_of_callbacks

    @classmethod
    async def send_object_to_callbacks(cls,callbacks_list:[CallBackClass],object):
        tasks=[]
        for callback in callbacks_list:
            callback:CallBackClass
            tasks.append(callback.callback_function(object))
        await asyncio.gather(*tasks)