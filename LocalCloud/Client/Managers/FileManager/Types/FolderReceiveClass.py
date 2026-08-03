from LocalCloud.Client.Server.FolderTokens import FolderTokens


class FolderReceiveClass(BaseException):
    def __init__(self,address,folder_name,folder_size,folder_token):
        self.address: str | None = address
        self.folder_name: str | None = folder_name
        self.folder_size:int|None = folder_size
        self.__folder_token:str|None=folder_token
    def save(self,*args):
        if len(args)==1:
            FolderTokens.add_path_to_token(token=self.__folder_token,folder_path=args[0])