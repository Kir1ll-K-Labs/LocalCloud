from LocalCloud import Server
Server.init() #инициализация сервера
#менеджеры при инициализации сами запускают сервер если он не был запущен ранее

#Server.white_list - белый список запросы приходящие от адресов которых нету в этом списке будут АВТОМАТИЧЕСКИ ОТКЛОНЕНЫ
print(Server.white_list) #Вывод {'localhost', '<ip адрес вашего устройства>', '127.0.0.1'} (последовательность может быть другой)

#удаление и добавление в whitelist
Server.remove_address_from_whitelist("localhost")
Server.add_address_to_whitelist("localhost")

fast_api_original_object = Server.fast_api_server #FastApi объект который создал сервер

uvicorn_server_object = Server.server_instance #Uvicorn Server объект который запустил FastApi

my_host=Server.current_host #хост (адрес) на котором работает LocalCloud

my_port=Server.current_port #порт на котором работает LocalCloud