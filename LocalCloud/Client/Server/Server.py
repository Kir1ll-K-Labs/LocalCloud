import asyncio
import threading
import socket
import urllib.parse
import os.path
import fastapi
import uvicorn
from fastapi import Response, UploadFile
from fastapi.params import File
import LocalCloud.Client.Managers.FileManager.Exceptions as api_exc

class Server:
    def __init__(self):
        pass
    @classmethod
    def load_json(cls,json):
        if "white_list" in json:
            white_list_set=set(json["white_list"])
            cls.white_list=white_list_set

        if "black_list" in json:
            black_list_set = set(json["black_list"])
            cls.black_list = black_list_set

        if "save_path" in json:
            cls.default_save_path=json["save_path"]

    @classmethod
    async def get_json(cls):
        return {
            "white_list":list(cls.white_list),
            "black_list":list(cls.black_list),
            "save_path":cls.default_save_path
        }

    @classmethod
    async def send_callbacks(cls, list, data):
        tasks = []
        for coroutine in list:
            tasks.append(coroutine(data))
        await asyncio.gather(*tasks)


    @classmethod
    def __init__class__(cls):
        if not hasattr(cls,"white_list"):
            cls.white_list = set()
        if not hasattr(cls,"black_list"):

            cls.black_list = set()
        if not hasattr(cls,"default_save_path"):
            cls.default_save_path = ""
        if not hasattr(cls,"on_file_receive_callbacks"):
            cls.on_file_receive_callbacks=[]
        if not hasattr(cls,"on_folder_receive_callbacks"):
            cls.on_folder_receive_callbacks=[]
        if not hasattr(cls, "on_file_receive_error_callbacks"):
            cls.on_file_receive_error_callbacks = []
        if not hasattr(cls, "on_folder_receive_error_callbacks"):
            cls.on_folder_receive_error_callbacks = []
        cls.started=False
    @classmethod
    def start_server(cls):
        if hasattr(cls,"server_instance") and cls.server_instance!=None:
            return
        cls.started=True
        cls.fast_api_server=fastapi.FastAPI()


        cls.white_list.add(socket.gethostbyname(socket.gethostname()))


        cls.current_host=socket.gethostbyname(socket.gethostname())
        cls.current_port=12123
        cls.server_instance:uvicorn.Server|None=None

        @cls.fast_api_server.get("/create_folder")
        async def create_folder(request: fastapi.Request):
            if cls.default_save_path=="":
                folder_receive_class_error=api_exc.FolderReceiveClassError()
                folder_receive_class_error.status_code=500
                await cls.send_callbacks(cls.on_folder_receive_error_callbacks,data=folder_receive_class_error)
                return Response(status_code=500,content="Ошибка на сервере")
            client_host = request.client.host
            if not client_host in cls.white_list:
                return Response(status_code=fastapi.status.HTTP_403_FORBIDDEN)
            relative_path = urllib.parse.unquote(request.headers.get("relative_path"), encoding="utf-8")
            folder_name=urllib.parse.unquote(request.headers.get("folder_name"), encoding="utf-8")
            folder_path=cls.default_save_path
            relative_path=eval(relative_path)
            for path in relative_path:
                folder_path=os.path.join(folder_path,path)
            folder_path=os.path.join(folder_path,folder_name)
            try:
                os.makedirs(folder_path)
                folder_receive_class=api_exc.FolderReceiveClass()
                folder_receive_class.folder_name=folder_name
                folder_receive_class.adres=client_host
                folder_receive_class.relative_path=relative_path
                folder_receive_class.status_code=200
                await cls.send_callbacks(list=cls.on_folder_receive_callbacks,data=folder_receive_class)
                return Response(status_code=200)
            except FileExistsError:
                return Response(status_code=200)
            finally:
                return Response(status_code=200)



        @cls.fast_api_server.post("/sent_file")
        async def on_sent_file(request: fastapi.Request, file: UploadFile = File(...)):
            client_host = request.client.host
            if not client_host in cls.white_list:
                return Response(status_code=fastapi.status.HTTP_403_FORBIDDEN)
            if cls.default_save_path=="":
                file_receive_class_error=api_exc.FileReceiveClassError()
                file_receive_class_error.adres=request.client.host
                file_receive_class_error.file_name=file.filename
                file_receive_class_error.status_code=500
                await cls.send_callbacks(list=cls.on_file_receive_error_callbacks,data=file_receive_class_error)
                return Response(status_code=500,content="Ошибка на сервере")
            content=await file.read()
            relative_path = urllib.parse.unquote(request.headers.get("relative_path"), encoding="utf-8")

            folder_path = cls.default_save_path
            relative_path = eval(relative_path)
            for path in relative_path:
                folder_path = os.path.join(folder_path, path)
            folder_path = os.path.join(folder_path, file.filename)
            with open(folder_path,"wb") as opened_file:
                try:
                    opened_file.write(content)
                    file_receive_class=api_exc.FileReceiveClass()
                    file_receive_class.adres=client_host
                    file_receive_class.file_name=file.filename
                    file_receive_class.relative_path=relative_path
                    file_receive_class.status_code=200
                    await cls.send_callbacks(list=cls.on_file_receive_callbacks,data=file_receive_class)
                except OSError as error:
                    file_receive_class_error=api_exc.FileReceiveClassError()
                    file_receive_class_error.adres=client_host
                    file_receive_class_error.file_name=file.filename
                    file_receive_class_error.status_code=500
                    file_receive_class_error.relative_path=relative_path
                    await cls.send_callbacks(list=cls.on_file_receive_error_callbacks,data=file_receive_class_error)
                    return Response(status_code=500,content="На диске целевого устройства закончилось место")
        """
        async def share_page(page:Page):
            page.title="input.txt"
            pass
        cls.fast_api_server.mount("/share",ft.fastapi.app(share_page))
        """
        @cls.fast_api_server.get("/echo")
        async def on_echo(request:fastapi.Request):
            client_host=request.client.host
            if not client_host in cls.white_list:
                return Response(status_code=fastapi.status.HTTP_403_FORBIDDEN,content=f"Ваш адрес ({client_host}) заблокирован на {cls.current_host}")
            if cls.default_save_path=="":
                return Response(status_code=fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR,content=f"На сервере произошла ошибка")
            return Response(status_code=fastapi.status.HTTP_200_OK)




        def start_inner():
            cls.server_instance=uvicorn.Server(config=uvicorn.Config(app=cls.fast_api_server,host="0.0.0.0",port=cls.current_port))
            cls.server_instance.run()

        threading.Thread(target=start_inner).start()
    @classmethod
    def stop_server(cls):
        def stop_inner():
            cls.server_instance.shutdown()
            cls.server_instance=None
        threading.Thread(target=stop_inner).start()