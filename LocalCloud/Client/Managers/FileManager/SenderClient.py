import os.path
import pathlib
import urllib.parse

import aiohttp
import asyncio

from .Exceptions.EchoException import EchoException
import LocalCloud.Client.Managers.FileManager.Exceptions as api_exc


class SenderClient:
    def __init__(self):
        pass

    @classmethod
    async def send_callbacks(cls, list, data):
        tasks = []
        for coroutine in list:
            tasks.append(coroutine(data))
        await asyncio.gather(*tasks)

    @classmethod
    def __init__class__(cls):
        if not hasattr(cls, "on_file_sent_callbacks"):
            cls.on_file_sent_callbacks = []

        if not hasattr(cls, "on_file_sent_error_callbacks"):
            cls.on_file_sent_error_callbacks = []

        if not hasattr(cls, "on_folder_sent_start_callbacks"):
            cls.on_folder_sent_start_callbacks = []
        if not hasattr(cls, "on_folder_sent_finish_callbacks"):
            cls.on_folder_sent_finish_callbacks = []
        if not hasattr(cls, "on_folder_sent_error_callbacks"):
            cls.on_folder_sent_error_callbacks = []

    @classmethod
    async def sent_echo(cls, addres: str):
        try:
            url = f"http://{addres}:12123/echo"
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=0.5) as response:
                    if response.status == 200:
                        return response.content
                    elif response.status == 500:
                        raise EchoException()
                    else:
                        raise EchoException()
        except asyncio.TimeoutError:
            raise EchoException(data=f"Не смогли подключиться к {addres}")
        except aiohttp.client_exceptions.InvalidUrlClientError:
            raise EchoException(data=f"{addres} не является корректным адресом")
        except aiohttp.client_exceptions.ClientConnectorDNSError:
            raise EchoException(data=f"{addres} нет подключения к {addres}")

    @classmethod
    async def create_folder(cls, addreses: [str], folder_name: str, relative_path):
        for addres in addreses:
            headers = {
                "relative_path": urllib.parse.quote(str(relative_path), encoding="utf-8"),
                "folder_name": urllib.parse.quote(str(folder_name), encoding="utf-8")
            }
            url = f"http://{addres}:12123/create_folder"
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=2, headers=headers) as response:
                    if response.status == 200:
                        folder_send_start = api_exc.FolderSendStart(addres=addres, folder_name=folder_name,
                                                                    relative_path=relative_path)
                        await cls.send_callbacks(list=cls.on_folder_sent_start_callbacks, data=folder_send_start)

                    else:
                        folder_sent_error = api_exc.FolderSentError(addres=addres, folder_name=folder_name,
                                                                    relative_path=relative_path)
                        raise folder_sent_error

    @classmethod
    async def _sent_file(cls, addreses: [str], file_path: str, relative_path):
        try:
            headers = {
                "relative_path": urllib.parse.quote(str(relative_path), encoding="utf-8")
            }
            # resp = requests.post(f"http://{addres}:12123/sent_file", headers=headers, files=files)
            async with aiohttp.ClientSession() as session:
                data = aiohttp.FormData()
                path = pathlib.Path(file_path)
                with path.open('rb') as f:

                    filename = os.path.basename(file_path)
                    content_type = filename[filename.rfind("."):]
                    data.add_field(
                        name='file',
                        value=f.read(),
                        filename=filename
                    )
                    for addres in addreses:
                        async with session.post(url=f"http://{addres}:12123/sent_file", headers=headers,
                                                data=data) as response:
                            if response.status == 200:
                                file_sent_class = api_exc.FileSentClass(status_code=response.status, file_name=filename,
                                                                        addres=addres, relative_path=relative_path)
                                file_sent_class.file_absolute_path = file_path
                                await cls.send_callbacks(list=cls.on_file_sent_callbacks, data=file_sent_class)

                            else:
                                file_sent_class_error = api_exc.FileSentClassError(status_code=response.status,
                                                                                   addres=addres,
                                                                                   relative_path=relative_path)
                                raise file_sent_class_error
        except asyncio.TimeoutError:
            file_sent_class_error = api_exc.FileSentClassError(status_code=403, addres=addres,
                                                               relative_path=relative_path)
            raise file_sent_class_error
        except OSError as error:
            file_sent_class_error = api_exc.FileSentClassError(status_code=response.status, addres=addres,
                                                               relative_path=relative_path)
            raise file_sent_class_error