from .TreeNode import TreeNode
from .FileNode import FileNode
from .FolderNode import FolderNode
import os.path
class MainNode:
    def __init__(self,base_path:str):
        self.total_files_count=0
        self.base_path=base_path
        self.childs:[TreeNode]=[]
    async def add_node(self,node:TreeNode):
        self.childs.append(node)
    async def remove_node(self,node:TreeNode):
        if node in self.childs:
            self.childs.remove(node)

    @classmethod
    async def __get_folder_node_by_path__(cls,folder_path,folder_name:str):
        folder_n = FolderNode(file_name=folder_name)
        with os.scandir(folder_path) as entries:
            for entry in entries:
                if entry.is_dir():
                    folder_node = await cls.__get_folder_node_by_path__(folder_path=os.path.join(folder_path, entry.name), folder_name=entry.name)
                    folder_n.childs.append(folder_node)
                    folder_n.total_files_count += folder_node.total_files_count
                if entry.is_file():
                    file_node = await cls.__get_file_node_by_name__(file_name=entry.name)
                    folder_n.childs.append(file_node)
                    folder_n.total_files_count += 1
        return folder_n

    @classmethod
    async def __get_file_node_by_name__(cls,file_name:str):
        file_node= FileNode(file_name=file_name)
        return file_node

    @classmethod
    async def get_mainnode_by_folder_path(cls,folder_path:str):
        if folder_path==None:
            raise RuntimeError("Путь папки не найден")
        main_node=MainNode(base_path=os.path.dirname(folder_path))
        file_name=os.path.basename(folder_path)
        folder_node = await cls.__get_folder_node_by_path__(folder_path=folder_path,folder_name=file_name)
        main_node.childs.append(folder_node)
        main_node.total_files_count += folder_node.total_files_count
        return main_node

    @classmethod
    async def get_mainnode_by_files_path(cls,file_paths:[str]):
        main_node=MainNode(base_path="")
        main_node.total_files_count=len(file_paths)
        for file_path in file_paths:
            file_node=FileNode(file_path=file_path)
            await main_node.add_node(file_node)
        return main_node