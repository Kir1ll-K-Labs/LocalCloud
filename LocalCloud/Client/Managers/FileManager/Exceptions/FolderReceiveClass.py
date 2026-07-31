class FolderReceiveClass(BaseException):
    def __init__(self):
        self.status_code: int | None = None
        self.adres: str | None = None
        self.folder_name: str | None = None
        self.relative_path: str | None = None