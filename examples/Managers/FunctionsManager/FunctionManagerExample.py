from datetime import datetime

#Импорт менеджера функций из LocalCloud и его типов данных
from LocalCloud import FunctionsManager,FunctionsManagerTypes
import asyncio
FunctionsManager.init() #инициализация менеджера перед началом работы
async def main():

    #функция для получения суммы переданных чисел (нужно написать на клиенте где будет вызываться)
    @FunctionsManager.on_invoke()
    async def summ_numbers(data:FunctionsManagerTypes.ReceivedFunction):

        len(data.args) #количество args элементов
        len(data.kwargs) #количество kwargs элементов
        numbers=data.args
        return sum(numbers)
    date1=datetime.now()
    summ_response=await FunctionsManager.invoke(
        FunctionsManagerTypes.InvokingFunction(
            address="localhost",#адрес устройства в локальной сети
            function_name="summ_numbers" #название функции которую нужно вызвать
        ),
        1,2,3
    )
    print(f"Сумма 1,2,3 = {summ_response}") #Выводит: 6
    print(datetime.now()-date1)

    #способ вызвать функцию на другом устройстве через ваш объект ассинхронной функции и адрес
    summ_response2=await summ_numbers.invoke_on_address("127.0.0.1",2,2)
    print(f"Сумма 2,2 = {summ_response2}")  # Выводит: 4


    #если в декораторе есть function_name:str то это будет использоваться в качестве имени функции
    @FunctionsManager.on_invoke(function_name="kwargs_fun")
    async def function_with_kwargs(data:FunctionsManagerTypes.ReceivedFunction):
        if "name" in data.kwargs:
            return f"Привет {data.name}!"
        else:
            return "Незнаю кому сказать привет."

    kwargs_response=await FunctionsManager.invoke(
        FunctionsManagerTypes.InvokingFunction(
            address="127.0.0.1",
            function_name="kwargs_fun"
        ),
        name="Kir1ll-K-Labs"
    )
    print(kwargs_response) #выводит: Привет Kir1ll-K-Labs!

    kwargs_response1 = await FunctionsManager.invoke(
        FunctionsManagerTypes.InvokingFunction(
            address="127.0.0.1",
            function_name="kwargs_fun"
        )
    )
    print(kwargs_response1) #Выводит: Незнаю кому сказать привет.

    #обрабатываем функции, в названии которых есть test
    @FunctionsManager.on_invoke(function_name=lambda name: "test" in name)
    async def test_functions_handler(data):
        return "Ответ от тестовой функции"

    test_response = await FunctionsManager.invoke(
        FunctionsManagerTypes.InvokingFunction(
            address="127.0.0.1",
            function_name="test_f"
        )
    )
    print(test_response)

    try:
        not_found_response = await FunctionsManager.invoke(
            FunctionsManagerTypes.InvokingFunction(
                address="127.0.0.1",
                function_name="unknown"
            )
        )
    except FunctionsManagerTypes.FunctionInvokeError as error:
        print("функция не выполнилась:")
        print(f"Причина: {error}")
asyncio.run(main())