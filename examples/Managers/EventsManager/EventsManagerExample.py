import asyncio
from LocalCloud import EventsManager,EventManagerTypes as etypes #импорт менеджера и его типов данных
EventsManager.init() #инициализация менеджера

#Обработчик для событий с name="echo"
@EventsManager.echo_event(name="echo")
async def on_event(event: etypes.ReceivedEvent):
    print("Получено echo событие")

#Обработчик для событий name которых начинается на
@EventsManager.echo_event(name=lambda n:n.startswith("с"))
async def on_event(event:etypes.ReceivedEvent):
    print("Получено событие name которого началось на с")

@EventsManager.echo_event() #обработчик по умолчанию
async def default_event_handler(event:etypes.ReceivedEvent):
    print("Другие обработчики неподошли и выполнился обработчик по умолчанию")

async def main():
    # _addresses_ - список адресов в локальной сети куда будет отправлено событие
    await EventsManager.send_event(_addresses_=["localhost"],name="echo") #Выполнится первый обработчик
    await EventsManager.send_event(_addresses_=["localhost"],name="с") #Выполнится второй обработчик
    await EventsManager.send_event(_addresses_=["localhost"], name="событие")  # Выполнится второй обработчик
    await EventsManager.send_event(_addresses_=["localhost"], name="")  # Выполнится обработчик по-умолчанию (третий)
    await EventsManager.send_event(_addresses_=["localhost"])  # Выполнится обработчик по-умолчанию (третий)


asyncio.run(main())