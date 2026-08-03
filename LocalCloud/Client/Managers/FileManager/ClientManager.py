from pathlib import Path

from .FileUploadTask import FileUploadTask
from .FilesTree.FileNode import FileNode
from .FilesTree.FolderNode import FolderNode
from .FilesTree.MainNode import MainNode
from .FilesTree.TreeNode import TreeNode
from .SenderClient import SenderClient

import os.path

import LocalCloud.Client.Managers.FileManager.Exceptions as api_exc

class ClientManager:
    def __init__(self):
        pass


    @classmethod
    def init(cls):
        cls.tasks_queue:[FileUploadTask]=[]

    @classmethod
    async def sent_folder_node(cls,addreses:[str],file_path:str,relative_path:[str],folder_node:FolderNode,folder_token=None,folder_size=None):
        try:
            response=await SenderClient.create_folder(addreses=addreses,folder_name=folder_node.file_name,relative_path=relative_path,folder_token=folder_token,folder_size=folder_size)
            if not response is None and "folder_token" in response:
                folder_token=response["folder_token"]
            relative_path = relative_path + [folder_node.file_name]
            for child in folder_node.childs:
                child: TreeNode
                if isinstance(child, FolderNode):
                    child: FolderNode
                    await cls.sent_folder_node(addreses=addreses, relative_path=relative_path,
                                               file_path=os.path.join(file_path, child.file_name), folder_node=child,folder_token=folder_token)
                elif isinstance(child, FileNode):
                    child: FileNode
                    await cls.sent_file_node(addreses=addreses, relative_path=relative_path,
                                            file_path=os.path.join(file_path, child.file_name), file_node=child,folder_token=folder_token)
        except api_exc.FolderSentError as error:
            error.folder_node=folder_node
            await SenderClient.send_callbacks(list=SenderClient.on_folder_sent_error_callbacks,data=error)

    @classmethod
    async def sent_file_node(cls,addreses:[str],file_path:str,relative_path,file_node:FileNode,folder_token=None):
        try:
            await SenderClient._sent_file(addreses=addreses,file_path=file_path,relative_path=relative_path,folder_token=folder_token)
        except api_exc.FileSentClassError as error:
            error.file_absolute_path=file_path
            await SenderClient.send_callbacks(list=SenderClient.on_file_sent_error_callbacks,data=error)

    @classmethod
    async def sent_main_node(cls,addreses:str,main_node:MainNode):
        for child in main_node.childs:
            child:TreeNode
            if isinstance(child,FileNode):
                child:FileNode
                file_path=""
                if hasattr(child,"file_name"):
                    file_path=os.path.join(main_node.base_path,child.file_name)
                elif hasattr(child,"file_path"):
                    file_path=child.file_path
                await cls.sent_file_node(addreses=addreses,relative_path=[],file_path=file_path,file_node=child)
            elif isinstance(child,FolderNode):
                child:FolderNode
                path=Path(os.path.join(main_node.base_path,child.file_name))
                folder_size=sum(f.stat().st_size for f in path.rglob('*') if f.is_file())
                resp=await cls.sent_folder_node(addreses=addreses,relative_path=[],file_path=os.path.join(main_node.base_path,child.file_name),folder_node=child,folder_size=folder_size)
    @classmethod
    async def __start_senting__(cls):
        while len(cls.tasks_queue)>0:
            next_task:FileUploadTask=cls.tasks_queue.pop()
            await cls.sent_main_node(addreses=next_task.addreses,main_node=next_task.main_node)

    @classmethod
    async def append(cls,file_upload_task:FileUploadTask):
        cls.tasks_queue.append(file_upload_task)
        await cls.__start_senting__()