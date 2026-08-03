from LocalCloud.Client.Server.Server import Server
from .SenderClient import SenderClient
from .Types.RemoteVariablesClass import RemoteVariablesClass
class VariablesManagerMeta(type):
    def init(cls):
        Server.init()
        Server._start_server()

    def __getitem__(self, item)->RemoteVariablesClass:
        return Server._variables_storage[item]

    def __setitem__(self, key, value):
        Server._variables_storage[key]=value
    def keys(cls):
        return Server._variables_storage.keys()

    def values(cls):
        return Server._variables_storage.values()

    def get_dict(cls):
        return Server._variables_storage
    def set_dict(cls,new_dict):
        Server.variables_storage=new_dict

    def items(cls):
        return Server._variables_storage.items()
    def pop(cls,key):
        return Server._variables_storage.pop(key)
    def setdefault(cls,key,default):
        Server._variables_storage.setdefault(key,default)

    async def have_local(cls,key):
        return key in Server._variables_storage

    async def get(cls,address,*args):
        remote_var_class=RemoteVariablesClass(address=address)
        return await remote_var_class.get(*args)

    async def get_local(cls,*args):
        value = None
        if len(args)==1:
            value=Server._variables_storage[args[0]]
        if len(args)==2:
            value=Server._variables_storage.get(args[0],args[1])
        if callable(value):
            return value()
        return value


class VariablesManager(metaclass=VariablesManagerMeta):
    pass