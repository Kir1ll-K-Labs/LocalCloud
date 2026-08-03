import asyncio

from LocalCloud import Server
Server.init()
async def main():
    #Чтобы другие устройства в локальной сети могли делать запросы на ваш Клиент
    #вам нужно добавить их в белый список (white_list)

    # добавляет адрес в белый список
    Server.add_address_to_whitelist("<локальный адресс устройства>")

    #удаляет адрес из белого списка True-если адрес был и удален, False - адреса не было.
    Server.remove_address_from_whitelist("<локальный адресс устройства>")

    white_list=Server.white_list #сам белый список, тип даннных set()
asyncio.run(main())


