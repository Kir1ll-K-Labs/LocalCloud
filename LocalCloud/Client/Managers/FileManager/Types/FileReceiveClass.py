import os


class FileReceiveClass(BaseException):
    def __init__(self):
        self.address: str | None = None
        self.file_name: str | None = None
        self.file_content=None
    def __str__(self):
        adres=self.address or "Незадан"
        file_name=self.file_name or "Незадано"
        return f"""Получен файл от {adres}
        Название: {file_name}
        """
    async def save(self,*args):
        if len(args)==1:
            file_path = os.path.join(args[0], self.file_name)
            with open(file_path, "wb") as opened_file:
                opened_file.write(self.file_content)