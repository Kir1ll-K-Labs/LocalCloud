import asyncio
from LocalCloud import EventsManager,EventManagerTypes
EventsManager.init()
async def main():
    #event_name это то что нужно указать при запросе сюда чтобы вызвать этот обработчик
    @EventsManager.echo_event(event_name="start_event")
    async def on_start(data:EventManagerTypes.ReceivedEvent):
        print(f"Получено событие start от {data.address}")
        print("Параметр:",data.custom_event_parameter)
    #события могут вызывать несколько обработчиков если они подходят
    @EventsManager.echo_event(event_name="start_event")
    async def on_start_two(data: EventManagerTypes.ReceivedEvent):
        print(f"Получено событие start в другом декораторе от {data.address}")
        print("Параметр:", data.custom_event_parameter)
    #если для обработчика не установлены фильтры он принимает все события кроме тех для которых есть подходящие обработчики
    @EventsManager.echo_event()
    async def on_default_event(data:EventManagerTypes.ReceivedEvent):
        print(f"У нас нет обработчика для {data.event_name}, но по умолчанию его обработали.")
    await EventsManager.send_event(
        EventManagerTypes.SendingEvent(
            addresses=["127.0.0.1"], #события могут быть отправлены на несколько адресов одновременно
            event_name="start_event" #название события на целевом адресе
        ),
        custom_event_parameter="Какой-то параметр")
    await EventsManager.send_event(
        EventManagerTypes.SendingEvent(
            addresses=["127.0.0.1"],
            event_name="custom_event"  # это обработается в обработчике по умолчанию
        ))
    await EventsManager.send_event(
        EventManagerTypes.SendingEvent(
            addresses=["127.0.0.1"],
            #запросы без указанного event_name так же ищут обработчик по умолчанию, в обработчике event_name будет =""
        ))
    #отпрпавление события от функции обработчика
    await on_start.send_to_addresses(["127.0.0.1"],custom_event_parameter="Получено при вызове через функцию обработчик")

    #декоратор с lambda параметром
    @EventsManager.echo_event(event_name=lambda name: name in ["событие1","событие2"])
    async def more_events(data:EventManagerTypes.ReceivedEvent):
        print("Получено событие в декораторе с lambda выражением")

    await EventsManager.send_event(
        EventManagerTypes.SendingEvent(
            addresses=["127.0.0.1"],
            event_name="событие1"
        ))
asyncio.run(main())