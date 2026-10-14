import asyncio
from LocalCloud import FunctionsManager,FunctionsManagerTypes #импорт менеджера и его типов данных
FunctionsManager.init() #инициализация менеджера
async def main():

    @FunctionsManager.on_invoke(function_name="sum") # обработчик функции с названием sum
    async def on_sum(data:FunctionsManagerTypes.ReceivedFunction):
        print(data.info) #Вывод "12"
        return sum(data.data)


    """
    Ранее уже был объявлен такой обработчик (этот не будет выполнятся)
    Общее правило для функций: если несколько функций одинаково подходят под запрос,
    То выполняется та которая была объявлена раньше
    """
    @FunctionsManager.on_invoke(function_name="sum")
    async def ons(data:FunctionsManagerTypes.ReceivedFunction):
        return None
    data=[2,3,4,5]
    function_responce = await FunctionsManager.invoke( #заппрос функции
        _address_="localhost",
        info="12",
        function_name="sum",
        data=data
    )
    print("Сумма:",function_responce.responce,function_responce.status_code) #Вывод "Сумма: 14 200"
asyncio.run(main())