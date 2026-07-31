
from .TreeNode import TreeNode

class FileNode(TreeNode):
    def __init__(self,file_name:str=None,file_path:str=None):
        super().__init__()
        if file_path!=None:
            self.file_path=file_path

        if file_name!=None:
            self.file_name=file_name
