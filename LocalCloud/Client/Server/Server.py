import asyncio
import json
import secrets
import threading
import socket
import urllib.parse
import os.path
import fastapi
import uvicorn
from fastapi import Response, UploadFile
from fastapi.params import File
import LocalCloud.Client.Managers.FileManager.Exceptions as api_exc
import LocalCloud.Client.Managers.FileManager.Types as api_types
import LocalCloud.Client.Managers.EventsManager.Types as events_types
import LocalCloud.Client.Managers.FunctionsManager.Types as function_typs
from LocalCloud.CallBackFilter import CallBackClass, CallBackFilter
from LocalCloud.Client.Managers.FileManager.Types import FileReceiveClass
from LocalCloud.Client.Server.FolderTokens import FolderTokens

class ServerMeta(type):
    @property
    def current_host(cls):
        return cls._c_host
    @property
    def current_port(cls):
        return cls._c_port
    @property
    def white_list(cls):
        return cls._white_list


class Server(metaclass=ServerMeta):
    _c_host=""
    _c_port=12
    _white_list=set()
    def __init__(self):
        pass
    @classmethod
    def add_address_to_whitelist(cls,address:str):
        cls._white_list.add(address)
    @classmethod
    def remove_address_from_whitelist(cls,address):
        if address in cls._white_list:
            cls._white_list.remove(address)
            return True
        return False
    @classmethod
    def _load_json(cls,json):
        if "white_list" in json:
            white_list_set=set(json["white_list"])
            cls._white_list=white_list_set

        if "save_path" in json:
            cls._default_save_path=json["save_path"]

    @classmethod
    async def _get_json(cls):
        return {
            "white_list":list(cls.white_list),
            "save_path":cls._default_save_path
        }

    @classmethod
    async def __send_callbacks(cls, list, data):
        tasks = []
        for coroutine in list:
            tasks.append(coroutine(data))
        await asyncio.gather(*tasks)


    @classmethod
    def init(cls):
        if not hasattr(cls,"_variables_storage"):
            cls._variables_storage={}
        if not hasattr(cls,"_white_list"):
            cls._white_list = set()
        if not hasattr(cls,"_default_save_path"):
            cls._default_save_path = ""
        if not hasattr(cls,"_on_file_receive_callbacks"):
            cls._on_file_receive_callbacks:[CallBackClass]=[]
        if not hasattr(cls,"_on_folder_receive_callbacks"):
            cls._on_folder_receive_callbacks:[CallBackClass]=[]
        if not hasattr(cls,"_on_event_receive_callbacks"):
            cls._on_event_receive_callbacks:[CallBackClass]=[]
        if not hasattr(cls,"_on_function_receive_callbacks"):
            cls._on_function_receive_callbacks:[CallBackClass]=[]
        cls._started=False
        cls._c_host = socket.gethostbyname(socket.gethostname())
        cls._c_port = 12123
        cls._start_server()
    @classmethod
    def _start_server(cls):
        if hasattr(cls,"server_instance") and cls.server_instance!=None:
            return
        cls.server_instance: uvicorn.Server | None = None
        cls._started=True
        cls.fast_api_server=fastapi.FastAPI()


        cls._white_list.add(socket.gethostbyname(socket.gethostname()))
        cls._white_list.add("127.0.0.1")
        cls._white_list.add("localhost")

        @cls.fast_api_server.get("/variables/get")
        async def variable_get(request:fastapi.Request):
            client_host = request.client.host
            if not client_host in cls._white_list:
                return Response(status_code=fastapi.status.HTTP_403_FORBIDDEN)
            key = urllib.parse.unquote(request.headers.get("key"), encoding="utf-8")
            if key in cls._variables_storage:
                value = cls._variables_storage[key]
                if callable(value):
                    value=value()
                try:
                    value=json.dumps(value)
                except TypeError:
                    value=json.dumps(str(value))
                return Response(status_code=200,content=value)
            else:
                return Response(status_code=404)
        @cls.fast_api_server.get("/function/get")
        async def functions_get(request:fastapi.Request):
            client_host = request.client.host
            if not client_host in cls._white_list:
                return Response(status_code=fastapi.status.HTTP_403_FORBIDDEN)
            function_data = urllib.parse.unquote(request.headers.get("function_data"), encoding="utf-8")
            received_function = function_typs.ReceivedFunction(address=client_host,function_data=function_data)
            availabled_callbacks = await CallBackFilter.get_available_callbacks(
                callbacks_list=cls._on_function_receive_callbacks, object=received_function)
            if len(availabled_callbacks)==0:
                return Response(status_code=404,content="На целевом адресе не найдено обработчиков функции")
            callback=availabled_callbacks[0]
            function_responce=await callback.callback_function(received_function)
            return Response(status_code=200,content=json.dumps(function_responce))
        @cls.fast_api_server.get("/events/get")
        async def events_get(request: fastapi.Request):
            client_host = request.client.host
            if not client_host in cls._white_list:
                return Response(status_code=fastapi.status.HTTP_403_FORBIDDEN)
            event_data = urllib.parse.unquote(request.headers.get("event_data"), encoding="utf-8")
            received_event=events_types.ReceivedEvent(address=client_host,event_data=event_data)
            availabled_callbacks=await CallBackFilter.get_available_callbacks(callbacks_list=cls._on_event_receive_callbacks,object=received_event)
            if len(availabled_callbacks)==0:
                return Response(status_code=404,content="Событие не было получено на целевом адресе")
            await CallBackFilter.send_object_to_callbacks(callbacks_list=availabled_callbacks,object=received_event)

        @cls.fast_api_server.get("/create_folder")
        async def create_folder(request: fastapi.Request):
            client_host = request.client.host
            if not client_host in cls._white_list:
                return Response(status_code=fastapi.status.HTTP_403_FORBIDDEN)
            relative_path = urllib.parse.unquote(request.headers.get("relative_path"), encoding="utf-8")
            folder_name=urllib.parse.unquote(request.headers.get("folder_name"), encoding="utf-8")
            relative_path=eval(relative_path)
            try:
                if len(relative_path)==0:
                    folder_token=secrets.token_hex(10)
                    folder_receive_class = api_types.FolderReceiveClass(address=client_host,folder_token=folder_token,folder_name=folder_name,folder_size=urllib.parse.unquote(request.headers.get("folder_size"), encoding="utf-8"))
                    availabled_callbacks = await CallBackFilter.get_available_callbacks(callbacks_list=cls._on_folder_receive_callbacks, object=folder_receive_class)
                    if len(availabled_callbacks) == 0:
                        return Response(status_code=404, content="Папка не была получена на целевом адресе")
                    await CallBackFilter.send_object_to_callbacks(callbacks_list=availabled_callbacks,object=folder_receive_class)
                    folder_paths = FolderTokens.get_paths_by_token(folder_token)
                    print(folder_paths)
                    if len(folder_paths) == 0:
                        return Response(status_code=404, content="Папка не была получена на целевом адресе")
                    for base_path in folder_paths:
                        folder_path = os.path.join(base_path, folder_name)
                        try:
                            os.makedirs(folder_path)
                        except FileExistsError:
                            pass
                    return Response(status_code=200,content=json.dumps({"folder_token":folder_token}))
                else:
                    folder_token=urllib.parse.unquote(request.headers.get("folder_token"))
                    folder_paths=FolderTokens.get_paths_by_token(folder_token)
                    for base_path in folder_paths:
                        folder_path=base_path
                        for path in relative_path:
                            folder_path = os.path.join(folder_path, path)
                        folder_path = os.path.join(folder_path, folder_name)

                        try:
                            os.makedirs(folder_path)
                        except FileExistsError:
                            pass
                    return Response(status_code=200,content='{}')
            except FileExistsError:
                pass



        @cls.fast_api_server.post("/sent_file")
        async def on_sent_file(request: fastapi.Request, file: UploadFile = File(...)):
            client_host = request.client.host
            if not client_host in cls._white_list:
                return Response(status_code=fastapi.status.HTTP_403_FORBIDDEN)
            content=await file.read()
            relative_path = urllib.parse.unquote(request.headers.get("relative_path"), encoding="utf-8")
            file_name=urllib.parse.unquote(file.filename)
            relative_path = eval(relative_path)
            if "folder_token" in request.headers:
                folder_token = urllib.parse.unquote(request.headers.get("folder_token"), encoding="utf-8")
                folders_paths=FolderTokens.get_paths_by_token(token=folder_token)
                for folder_path in folders_paths:
                    for path in relative_path:
                        folder_path = os.path.join(folder_path, path)
                    folder_path = os.path.join(folder_path, file_name)
                    with open(folder_path,"wb") as opened_file:
                        try:
                            opened_file.write(content)
                        except OSError as error:
                            return Response(status_code=500,content="На диске целевого устройства закончилось место")
                return Response(status_code=200,content="{}")
            else:
                file_receive_class=FileReceiveClass()
                file_receive_class.file_name=file_name
                file_receive_class.address=client_host
                file_receive_class.file_content=content
                availabled_callbacks = await CallBackFilter.get_available_callbacks(
                    callbacks_list=cls._on_file_receive_callbacks, object=file_receive_class)
                if len(availabled_callbacks)==0:
                    return Response(status_code=404,content="Целевой Клиент не принял этот файл")
                await CallBackFilter.send_object_to_callbacks(callbacks_list=availabled_callbacks,
                                                              object=file_receive_class)
        """
        async def share_page(page:Page):
            page.title="input.txt"
            pass
        cls.fast_api_server.mount("/share",ft.fastapi.app(share_page))
        """
        @cls.fast_api_server.get("/echo")
        async def on_echo(request:fastapi.Request):
            client_host=request.client.host
            if not client_host in cls._white_list:
                return Response(status_code=fastapi.status.HTTP_403_FORBIDDEN,content=f"Ваш адрес ({client_host}) заблокирован на {cls.current_host}")
            if cls._default_save_path=="":
                return Response(status_code=fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR,content=f"На сервере произошла ошибка")
            return Response(status_code=fastapi.status.HTTP_200_OK)




        def start_inner():
            cls.server_instance=uvicorn.Server(config=uvicorn.Config(app=cls.fast_api_server,host="0.0.0.0",port=cls.current_port,access_log=True))
            cls.server_instance.run()

        threading.Thread(target=start_inner).start()
    @classmethod
    def stop_server(cls):
        async def stop_inner():
            await  cls.server_instance.shutdown()
            cls.server_instance=None
        asyncio.run(stop_inner())