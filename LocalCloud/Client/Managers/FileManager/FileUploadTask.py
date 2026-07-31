from LocalCloud.Client.Managers.FileManager.FilesTree.MainNode import MainNode


class FileUploadTask:
    def __init__(self,addreses:[str],main_node:MainNode):
        self.addreses=addreses
        self.main_node:MainNode=main_node