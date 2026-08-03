import asyncio

from LocalCloud import FileManager,FileManagerTypes
#запуск файлового менеджера
FileManager.init()
async def main():
    @FileManager.on_folder_receive()
    async def on_folder_receive(data:FileManagerTypes.FolderReceiveClass):
        #указываем путь куда будет сохранена папка
        data.save("<тут ваш путь на диске>")

    @FileManager.on_folder_receive(folder_name=lambda name: name.startswith("test"))
    async def on_folder_receive_test(data: FileManagerTypes.FolderReceiveClass):
        # указываем путь, куда будет сохранена папка имя которой начинается на test
        data.save("<тут ваш путь на диске>")
        """
        #так тоже можно
        if data.folder_name.startswith("test"):
            data.save("<тут ваш путь на диске>")
        """
    @FileManager.on_file_receive()
    async def on_file_receive(data:FileManagerTypes.FileReceiveClass):
        await data.save("<путь на диске куда будет сохранен файл>")
    #группа отправлений
    #содержит адреса и файлы/папки для отправлений
    sending_group = await FileManager.create_sending_group()
    await sending_group.add_address("107.0.0.1",check_address=False)
    #добавление файлов
    await sending_group.add_files(
        "<путь к файлу 1>",
        "<путь к файлу 2>",
        "<путь к файлу N>"
    )
    #добавление папки
    await sending_group.add_folder("<путь к папке на диске которую надо отправить>")
    await sending_group.start_sending()

asyncio.run(main())