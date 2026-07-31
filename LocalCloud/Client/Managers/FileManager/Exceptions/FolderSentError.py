from LocalCloud.Client.Managers.FileManager.FilesTree.FolderNode import FolderNode


class FolderSentError(BaseException):
    def __init__(self,addres,folder_name,relative_path):
        self.addres=addres
        self.folder_name=folder_name
        self.relative_path=relative_path
        self.folder_node:FolderNode|None=None