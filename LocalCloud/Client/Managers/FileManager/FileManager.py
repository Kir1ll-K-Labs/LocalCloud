from .SendingGroup import SendingGroup
from LocalCloud.Client.Server import Server
from .SenderClient import SenderClient
from .ClientManager import ClientManager
class FileManager:
    @classmethod
    def __init__class(cls):
        SenderClient.__init__class__()
        Server.__init__class__()
        ClientManager.__init__class__()


    @classmethod
    async def create_sending_group(cls) -> SendingGroup:
        senting_group = SendingGroup()
        return senting_group

    @classmethod
    async def set_default_save_path(cls, path: str):
        Server.default_save_path = path

    @classmethod
    def __init__class__(cls):
        Server.__init__class__()
        SenderClient.__init__class__()
        ClientManager.__init__class__()
        if not Server.started:
            Server.start_server()

    @classmethod
    async def is_addres_available(cls, addres: str):
        await SenderClient.sent_echo(addres=addres)

    @classmethod
    def on_file_received(cls, function):
        if not hasattr(Server, "on_file_receive_callbacks"):
            Server.on_file_receive_callbacks = []
        Server.on_file_receive_callbacks.append(function)

    @classmethod
    def on_file_received_error(cls, function):
        if not hasattr(Server, "on_file_receive_error_callbacks"):
            Server.on_file_receive_error_callbacks = []
        Server.on_file_receive_error_callbacks.append(function)

    @classmethod
    def on_file_sent(cls, function):
        if not hasattr(SenderClient, "on_file_sent_callbacks"):
            SenderClient.on_file_sent_callbacks = []
        SenderClient.on_file_sent_callbacks.append(function)

    @classmethod
    def on_file_sent_error(cls, function):
        if not hasattr(SenderClient, "on_file_sent_error_callbacks"):
            SenderClient.on_file_sent_error_callbacks = []
        SenderClient.on_file_sent_error_callbacks.append(function)

    @classmethod
    def on_folder_received(cls, function):
        if not hasattr(Server, "on_folder_receive_callbacks"):
            Server.on_folder_receive_callbacks = []
        Server.on_folder_receive_callbacks.append(function)

    @classmethod
    def on_folder_received_error(cls, function):
        if not hasattr(Server, "on_folder_receive_error_callbacks"):
            Server.on_folder_receive_error_callbacks = []
        Server.on_folder_receive_error_callbacks.append(function)

    @classmethod
    def on_folder_sent_start(cls, function):
        if not hasattr(SenderClient, "on_folder_sent_start_callbacks"):
            SenderClient.on_folder_sent_start_callbacks = []
        SenderClient.on_folder_sent_start_callbacks.append(function)

    @classmethod
    def on_folder_sent_finish(cls, function):
        if not hasattr(SenderClient, "on_folder_sent_finish_callbacks"):
            SenderClient.on_folder_sent_finish_callbacks = []
        SenderClient.on_folder_sent_finish_callbacks.append(function)

    @classmethod
    def on_folder_sent_error(cls, function):
        if not hasattr(SenderClient, "on_folder_sent_error_callbacks"):
            SenderClient.on_folder_sent_error_callbacks = []
        SenderClient.on_folder_sent_error_callbacks.append(function)