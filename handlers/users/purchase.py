from aiogram import Router, types
from aiogram.filters import Command
import requests
import xml.etree.ElementTree as ET

purchase_router = Router()

# Асинхронная функция для обработки команды /rates
@purchase_router.message(Command(commands=["rates"]))
async def send_exchange_rates(message: types.Message):
    url = "https://www.cbr.ru/scripts/XML_daily.asp"  # URL для получения курсов валют от Центрального Банка России
    response = requests.get(url)  # Выполнение GET-запроса к указанному URL
    if response.status_code == 200:  # Проверка успешности запроса
        # Парсинг XML ответа
        tree = ET.ElementTree(ET.fromstring(response.content))  # Создание XML дерева из содержимого ответа
        root = tree.getroot()  # Получение корневого элемента XML дерева
        rates = {}  # Словарь для хранения курсов валют
        for valute in root.findall('Valute'):  # Поиск всех элементов Valute в XML
            char_code = valute.find('CharCode').text  # Получение кода валюты
            value = float(
                valute.find('Value').text.replace(',', '.'))  # Получение и преобразование значения курса валюты
            if char_code in ['USD', 'TRY', 'EUR']:  # Проверка, интересует ли нас эта валюта
                rates[char_code] = value  # Добавление курса валюты в словарь

        # Получение курсов валют из словаря или значение 'N/A', если курс не найден
        usd_rate = rates.get('USD', 'N/A')
        try_rate = rates.get('TRY', 'N/A')
        eur_rate = rates.get('EUR', 'N/A')

        # Отправка сообщения пользователю с текущими курсами валют
        await message.answer(
            f"Текущие курсы валют:\n"
            f"1 USD = {usd_rate:.2f} RUB\n"
            f"1 TRY = {try_rate:.2f} RUB\n"
            f"1 EUR = {eur_rate:.2f} RUB"
        )
    else:
        # Отправка сообщения об ошибке, если запрос не был успешен
        await message.answer("Не удалось получить курсы валют. Попробуйте позже.")
