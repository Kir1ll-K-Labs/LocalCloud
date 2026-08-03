
from .TreeNode import TreeNode
class FolderNode(TreeNode):
    def __init__(self, file_name:str,file_path:str=None):
        super().__init__()
        self.file_name:str=file_name
        self.total_files_count=0
        self.file_path:str=file_path
        self.file_size=0
        self.childs:[TreeNode]=[]
    async def add_child(self,node:TreeNode):
        self.childs.append(node)
    async def remove_child(self,node:TreeNode):
        if node in self.childs:
            self.childs.remove(node)