
class FileSentClassError(BaseException):
    def __init__(self,status_code,addres,relative_path):
        self.status_code=status_code
        self.adres=addres
        self.relative_path=relative_path
        self.file_absolute_path:str|None=None