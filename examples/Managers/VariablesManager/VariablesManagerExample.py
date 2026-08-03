import asyncio
from datetime import datetime

from LocalCloud import VariablesManager,VariablesManagerTypes
VariablesManager.init()
async def main():
    #Добавляем переменную в доступ из локальной сети
    name="Kir1ll-K-Labs"
    VariablesManager["name"]=name
    print(await VariablesManager.get("127.0.0.1","name"))#запрашиваем переменную

    try:
        print(await VariablesManager.get("127.0.0.1", "main_name"))
    except KeyError:
        print("Если переменной нет на целевом клиенте создастся исключение KeyError")

    print(await VariablesManager.get("127.0.0.1", "main_name","значение по умолчание если key не найден на целевом клиенте"))

    count=1
    #оберните переменную в лямбда-функцию если нужно сохранять её актуальность
    VariablesManager["count"]=lambda:count
    count=5 #переменная поменялась но lambda запросит актуальное значение переменной при запросе

    print(f"count = {await VariablesManager.get("127.0.0.1", "count")}")

    VariablesManager["current_time"]=lambda:datetime.now()

    print(f"Текущая дата/время: { await VariablesManager.get("127.0.0.1", "current_time")}")

    # методы ниже относятся к внутреннему словарю данных
    print(f"keys= {VariablesManager.keys()}") #список ключей (dict_keys) в словаре
    print(f"items= {VariablesManager.items()}") # список (dict_items)
    print(f"values= {VariablesManager.values()}")#список значений (dict_values) в словаре
    print(f"pop= {VariablesManager.pop("count")}")#удаляет элемент из словаря

    #будьте осторожны с методами ниже
    VariablesManager.get_dict()#получает весь словарь целиком
    VariablesManager.set_dict(new_dict={})#устанавливает новый словарь в память библиотеки
asyncio.run(main())