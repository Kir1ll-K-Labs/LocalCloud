class Handlers:
    def __init__(self,handlers_list):
        self.__innerlist=handlers_list

    def __getitem__(self, item):
        return self.__innerlist[item]
    def __add__(self, other):
        if not isinstance(other,Handlers):
            raise RuntimeError("Handlers может складываться только с Handlers")
        return Handlers(self.__innerlist+other.__innerlist)

    def filter(self,*args,**kwargs):
        c_weight = -1
        c_list_of_callbacks = []
        for callback in self.__innerlist:
            weight = 0
            for key, value in callback.kwargs.items():
                if key not in kwargs:
                    weight = -1
                    break
                cur_val = kwargs[key]
                if callable(cur_val) and not isinstance(cur_val,type):
                    if cur_val(callback.kwargs.get(key)):
                        weight += 1
                    else:
                        weight = -1
                        break
                    continue
                if cur_val != value:
                    weight = -1
                    break
                weight += 1
            if weight<0:
                continue
            if weight > c_weight:
                c_list_of_callbacks = [callback]
                c_weight = weight
            elif weight == c_weight:
                c_list_of_callbacks.append(callback)


        return Handlers(handlers_list=c_list_of_callbacks)

    def __len__(self):
        return len(self.__innerlist)