class FolderTokens:
    @classmethod
    def init(cls):
        cls.token_storage={}
    def __init__(self):
        pass
    @classmethod
    def add_path_to_token(cls,token:str,folder_path:str):
        if not token in cls.token_storage:
            cls.token_storage[token]=[]
        cls.token_storage[token].append(folder_path)
    @classmethod
    def get_paths_by_token(cls,token:str):
        return cls.token_storage.get(token,[])