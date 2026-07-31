class FolderSendStart(BaseException):
    def __init__(self,addres,folder_name,relative_path):
        self.addres=addres
        self.folder_name=folder_name
        self.relative_path=relative_path