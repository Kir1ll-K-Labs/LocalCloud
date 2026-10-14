import LocalCloud
from LocalCloud import FunctionsManager, EventsManager, Server

FunctionsManager.init()
EventsManager.init()
@FunctionsManager.on_invoke() #если function_name отсутствует то он берется от названия функции обработчики
async def on_summ(data): #в этом примере function_name="on_summ"
    return sum(data.int_list)

@EventsManager.echo_event()
async def on_event(event):
    pass

all_project_handlers = LocalCloud.get_all_handlers() #получить все обработчики в LocalCloud

functions_handlers = FunctionsManager.get_handlers() #получить обработчики только FunctionsManager

events_handlers = EventsManager.get_handlers() #получить обработчики только EventsManager
print(len(all_project_handlers)) # Вывод 2
print(len(functions_handlers)) # Вывод 1
print(len(events_handlers)) # Вывод 1

for handler in all_project_handlers: #обработчики можно перебирать внутири циклов
    print(handler.kwargs) #фильтры обработчика (там где строки 6 и 10 то что в скобках было)
    print(handler.callback_function) #обьект async функции которая вызывается когда обработчик будет вызван
