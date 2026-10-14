import asyncio
from LocalCloud import FileManager,FileManagerTypes #импорт менеджера и его типов данных
FileManager.init() #инициализация менеджера


async def main():
    #Обработчик для получения файлов
    @FileManager.on_file_receive()
    async def on_file(file:FileManagerTypes.FileReceiveClass):
        print(file.file_name) #названине файла
        print(file.address) #адрес откуда файл получен
        await file.save("<путь на диске>") #путь для сохранения файла

    #Обработчик для получения файлов
    @FileManager.on_folder_receive()
    async def on_folder(folder:FileManagerTypes.FolderReceiveClass):
        folder.save("<путь на диске>") #путь для сохранения папки


    await FileManager.send( # send - функция отправления файлов/папок
        ["<IP адрес устройства куда будет сделан запрос>"],#список адресов:[str] в первом аргументе
        FileManagerTypes.File("./inputs/input.txt"), #класс для описания файла
        FileManagerTypes.Folder("./inputs") #класс для описания папки
    )

asyncio.run(main())