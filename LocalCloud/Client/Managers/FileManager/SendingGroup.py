from .ClientManager import ClientManager
from .FileUploadTask import FileUploadTask
from .FilesTree.MainNode import MainNode
from .SenderClient import SenderClient
class SendingGroup:
    def __init__(self):
        self.client=SenderClient
        self.addresses=[]
        self.main_nodes=[]

    async def add_address(self,address:str,check_address=True):
        if not address in self.addresses:
            if check_address:
                await SenderClient.sent_echo(addres=address)
            self.addresses.append(address)
    async def remove_address(self,address:str):
        if address in self.addresses:
            self.addresses.remove(address)
    async def add_files(self,*files_path:[str]):
        main_node = await MainNode.get_mainnode_by_files_path(file_paths=files_path)
        self.main_nodes.append(main_node)

    async def add_folder(self,folder_path:str):
        main_node = await MainNode.get_mainnode_by_folder_path(folder_path=folder_path)
        self.main_nodes.append(main_node)
    async def remove_all_addreses(self):
        self.addresses.clear()
    async def start_sending(self):
        for node in self.main_nodes:
            file_upload_task = FileUploadTask(addreses=self.addresses, main_node=node)
            await ClientManager.append(file_upload_task=file_upload_task)
    async def get_files_count(self):
        count=0
        for node in self.main_nodes:
            count+=node.total_files_count
        return count