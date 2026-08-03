class CallBackClass:
    def __init__(self,function,kwargs):
        self.callback_function=function
        self.kwargs=kwargs

    async def get_weight(self,object):
        weight=0
        for key,value in self.kwargs.items():
            cur_val = getattr(object,key,None)
            if cur_val is None and not hasattr(object,key):
                return -1
            if callable(value):
                if value(cur_val):
                    weight+=1
                else:
                    return -1
                continue
            if cur_val!=value:
                return -1
            weight+=1
        return weight