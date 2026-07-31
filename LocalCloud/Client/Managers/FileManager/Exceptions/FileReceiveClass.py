class FileReceiveClass(BaseException):
    def __init__(self):
        self.status_code: int | None = None
        self.adres: str | None = None
        self.file_name: str | None = None
        self.relative_path: str | None = None
    def __str__(self):
        status_code=self.status_code or "Незадан"
        adres=self.adres or "Незадан"
        file_name=self.file_name or "Незадано"
        relative_path=self.relative_path or "Незадан"
        return f"""Получен файл от {adres}
        Название: {file_name}
        Относительный путь: {relative_path}
        Отправленный сетевой код: {status_code}
        """