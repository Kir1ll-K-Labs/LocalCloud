from LocalCloud.CallBackFilter import CallBackClass
from LocalCloud.CallBackFilter.Handlers import Handlers
from LocalCloud.Client.Server import Server
from .SenderClient import SenderClient
from .ClientManager import ClientManager
from .SendingGroup import SendingGroup
from ...Server.FolderTokens import FolderTokens
from .Types.Folder import Folder
from .Types.File import File


class FileManager:

    @classmethod
    def __init__class(cls):
        SenderClient.init()
        Server.init()
        ClientManager.init()

    @classmethod
    async def set_default_save_path(cls, path: str):
        Server.default_save_path = path

    @classmethod
    def get_file_handlers(cls) -> Handlers:
        return Handlers(handlers_list=Server._on_file_receive_callbacks)

    @classmethod
    def get_folder_handlers(cls) -> Handlers:
        return Handlers(handlers_list=Server._on_folder_receive_callbacks)

    @classmethod
    async def send(cls,addresses,*args:[File|Folder]):
        sending_group = SendingGroup()
        sending_group.addresses=addresses
        for element in args:
            if isinstance(element,File):
                await sending_group.add_files(*[element.path_to_file])
            elif isinstance(element,Folder):
                await sending_group.add_folder(element.path_to_folder)
        await sending_group.start_sending()
    @classmethod
    def init(cls):
        Server.init()
        SenderClient.init()
        FolderTokens.init()
        ClientManager.init()
        if not Server._started:
            Server._start_server()

    @classmethod
    async def is_addres_available(cls, addres: str):
        await SenderClient.sent_echo(addres=addres)

    @classmethod
    def on_file_receive(cls, **kwargs):
        def decorator(function):
            call_back_class = CallBackClass(function=function, kwargs=kwargs)
            Server._on_file_receive_callbacks.append(call_back_class)
            return function
        return decorator

    @classmethod
    def on_file_sent_error(cls, function):
        if not hasattr(SenderClient, "_on_file_sent_error_callbacks"):
            SenderClient._on_file_sent_error_callbacks = []
        SenderClient._on_file_sent_error_callbacks.append(function)

    @classmethod
    def on_folder_receive(cls, **kwargs):
        def decorator(function):
            call_back_class = CallBackClass(function=function, kwargs=kwargs)
            if not hasattr(Server, "_on_folder_receive_callbacks"):
                Server._on_folder_receive_callbacks = []
            Server._on_folder_receive_callbacks.append(call_back_class)
            return function
        return decorator
    @classmethod
    def on_folder_received_error(cls, function):
        if not hasattr(Server, "_on_folder_receive_error_callbacks"):
            Server._on_folder_receive_error_callbacks = []
        Server._on_folder_receive_error_callbacks.append(function)

    @classmethod
    def on_folder_sent_start(cls, function):
        if not hasattr(SenderClient, "_on_folder_sent_start_callbacks"):
            SenderClient._on_folder_sent_start_callbacks = []
        SenderClient._on_folder_sent_start_callbacks.append(function)

    @classmethod
    def on_folder_sent_finish(cls, function):
        if not hasattr(SenderClient, "_on_folder_sent_finish_callbacks"):
            SenderClient._on_folder_sent_finish_callbacks = []
        SenderClient._on_folder_sent_finish_callbacks.append(function)

    @classmethod
    def on_folder_sent_error(cls, function):
        if not hasattr(SenderClient, "_on_folder_sent_error_callbacks"):
            SenderClient._on_folder_sent_error_callbacks = []
        SenderClient._on_folder_sent_error_callbacks.append(function)