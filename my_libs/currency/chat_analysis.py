import os
import re
from datetime import datetime, timedelta, timezone
from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from configparser import ConfigParser
import pandas as pd
import requests
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,  # Уровень логирования
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Формат сообщений
    handlers=[
        logging.FileHandler("app.log"),  # Запись логов в файл
        logging.StreamHandler()  # Вывод логов на консоль
    ]
)

# Путь к папке data
data_dir = 'data'
chats_file = os.path.join(data_dir, 'chats.txt')

# Регулярное выражение для определения начала нового сообщения (дата и время в формате YYYY-MM-DD HH:MM:SS UTC)
message_start_re = re.compile(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} UTC')

# Регулярное выражение для фильтрации сообщений и поиска цены
# Ищем сообщения, где упоминаются "синие" или "белые" доллары и фраза
# "по <цена>". Допускаем 2-3 цифры и необязательную десятичную часть,
# разделённую запятой, точкой, символом "^", пробелом или "р".
# В выражении одна захватывающая группа возвращает саму цену.
filter_re = re.compile(
    r'(?:син\w*|бел\w*)[^\n]*?по\s+(\d{2,3}(?:[.,^\sр]?\d{1,2})?)',
    re.IGNORECASE,
)

# Список для хранения дат и цен
dates_and_prices = []
# Список сообщений, прошедших фильтр и использованных при расчётах
filtered_messages = []

# Функция для проверки, содержит ли сообщение ключевые слова для игнорирования
def contains_ignore_keywords(message):
    message_lower = message.lower()
    # Строки, по которым сообщения нужно игнорировать полностью
    ignore_keywords = ['usdt', 'махачкала', '€', 'евро']

    # Отдельная проверка на варианты написания "115 ФЗ"
    if re.search(r'115[\s-]?фз', message_lower):
        return True

    return any(keyword in message_lower for keyword in ignore_keywords)

# Функция для чтения и отображения содержимого файла с сообщениями чата
def display_chat_messages(chat_file):
    def process_message(message):
        if filter_re.search(message) and not contains_ignore_keywords(message):
            print(message)
            date_match = message_start_re.match(message)
            price_match = filter_re.search(message)
            if date_match and price_match:
                date = date_match.group(0)
                price_raw = price_match.group(2).replace(',', '.').replace('^', '.').replace('р', '.').replace(' ', '.')
                try:
                    price = f'{float(price_raw):.2f}'  # Форматируем цену с двумя десятичными знаками
                    dates_and_prices.append((date, price))
                    filtered_messages.append(message)
                except ValueError as e:
                    logging.error(f'Error parsing price: {e}')
            else:
                logging.warning(f'Invalid message format: {message}')

    with open(chat_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        current_message = []

        for line in lines:
            if message_start_re.match(line):
                if current_message:
                    full_message = ' '.join(current_message).strip()
                    process_message(full_message)
                    current_message = []
            current_message.append(line.strip())

        if current_message:
            full_message = ' '.join(current_message).strip()
            process_message(full_message)
async def export_messages(chat_id, chat_name):
    now = datetime.now(timezone.utc)
    one_week_ago = now - timedelta(days=7)
    offset_id = 0
    limit = 100

    all_messages = []

    while True:
        history = await client(GetHistoryRequest(
            peer=chat_id,
            offset_id=offset_id,
            offset_date=None,
            add_offset=0,
            limit=limit,
            max_id=0,
            min_id=0,
            hash=0
        ))

        if not history.messages:
            break

        messages = history.messages

        for message in messages:
            if message.date.replace(tzinfo=timezone.utc) < one_week_ago:
                break
            all_messages.append(message)

        offset_id = messages[-1].id

        if messages[-1].date.replace(tzinfo=timezone.utc) < one_week_ago:
            break

    # Сохраняем сообщения в файл, добавляя новые записи
    chat_file = os.path.join(data_dir, f'{chat_name}.txt')
    existing_lines = set()
    if os.path.exists(chat_file):
        with open(chat_file, 'r', encoding='utf-8') as f:
            existing_lines = {line.strip() for line in f if line.strip()}

    with open(chat_file, 'a', encoding='utf-8') as f:
        for message in all_messages:
            text = (message.message or '').replace('\n', ' ').replace('\r', ' ')
            line = f"{message.date.strftime('%Y-%m-%d %H:%M:%S %Z')} - {message.sender_id}: {text}"
            if line not in existing_lines:
                f.write(line + '\n')

# Главная функция для чтения файла chats.txt и экспорта сообщений
async def export_main():
    with open(chats_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            chat_id, chat_name = line.strip().split(' - ')
            chat_id = int(chat_id)
            print(f'Экспорт сообщений для чата: {chat_name}')
            await export_messages(chat_id, chat_name)
            print(f'Сообщения для чата {chat_name} успешно экспортированы.')

# Главная функция для отображения сообщений из всех файлов чатов
def analyze_main():
    # Проверяем, существует ли папка data
    if not os.path.exists(data_dir):
        print("Папка data не существует. Убедитесь, что папка data и файлы с сообщениями чатов существуют.")
        return

    # Получаем список файлов в папке data
    chat_files = [f for f in os.listdir(data_dir) if f.endswith('.txt')]

    if not chat_files:
        print("Нет файлов с сообщениями чатов в папке data.")
        return

    # Читаем и отображаем сообщения из каждого файла
    for chat_file in chat_files:
        print(f"\nСообщения из чата: {chat_file}")
        display_chat_messages(os.path.join(data_dir, chat_file))

    # Сортируем список дат и цен
    sorted_dates_and_prices = sorted(dates_and_prices, key=lambda x: datetime.strptime(x[0], '%Y-%m-%d %H:%M:%S UTC'))

    # Выводим отсортированный список дат и цен
    print("\nСписок дат и цен:")
    for date, price in sorted_dates_and_prices:
        print(f'{date}: {price}')

    # Записываем все отфильтрованные сообщения в отдельный файл,
    # сортируя их по дате от старых к новым и помечая используемую цену
    messages_file = os.path.join(data_dir, 'used_messages.txt')

    def strip_price_tag(line):
        """Удаляем ранее добавленную отметку цены в конце сообщения."""
        return re.sub(r'\s\[\d{2,3}(?:\.\d{2})?\]$', '', line)

    existing_lines = []
    if os.path.exists(messages_file):
        with open(messages_file, 'r', encoding='utf-8') as f:
            existing_lines = [strip_price_tag(l.strip()) for l in f if l.strip()]

    existing_set = set(existing_lines)
    for msg in filtered_messages:
        base_msg = strip_price_tag(msg)
        if base_msg not in existing_set:
            existing_lines.append(base_msg)
            existing_set.add(base_msg)

    def parse_date(line: str):
        m = message_start_re.match(line)
        if m:
            return datetime.strptime(m.group(0), '%Y-%m-%d %H:%M:%S UTC')
        return datetime.min

    existing_lines.sort(key=parse_date)

    def annotate_price(line: str):
        m = filter_re.search(line)
        if m:
            raw = m.group(1).replace(',', '.').replace('^', '.').replace('р', '.')
            try:
                price = f"{float(raw):.2f}"
                return f"{line} [{price}]"
            except ValueError:
                return line
        return line

    with open(messages_file, 'w', encoding='utf-8') as f:
        for line in existing_lines:
            f.write(annotate_price(line) + '\n')
    return sorted_dates_and_prices

# Функция для вычисления средних цен за каждый день
def calculate_daily_average(prices):
    # Создаем DataFrame из списка цен
    df = pd.DataFrame(prices, columns=['datetime', 'price'])

    # Преобразуем столбец 'datetime' в формат datetime и 'price' в формат float
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['price'] = df['price'].astype(float)

    # Группируем данные по дате
    df['date'] = df['datetime'].dt.date
    grouped = df.groupby('date')['price']

    # Вычисляем среднюю цену с учетом стандартного отклонения
    daily_averages = []
    for date, group in grouped:
        # Вычисляем среднее и стандартное отклонение
        mean = group.mean()
        std = group.std()
        print(std)

        # Фильтруем данные, оставляя только значения в пределах одного стандартного отклонения
        filtered_group = group[(group >= mean - std) & (group <= mean + std)]

        # Вычисляем новое среднее значение после фильтрации
        new_mean = filtered_group.mean()
        daily_averages.append((str(date), f'{new_mean:.2f}'))

    return daily_averages

def update_currency_rates(dates_and_rates):
    # Путь к файлу с курсами валют
    currency_file = 'data/currency.txt'

    # Функция для получения курса ЦБ РФ на указанную дату
    def get_cbr_rate(date):
        response = requests.get(f'https://www.cbr.ru/scripts/XML_daily.asp?date_req={date.strftime("%d/%m/%Y")}')
        if response.status_code == 200:
            from xml.etree import ElementTree as ET
            tree = ET.fromstring(response.content)
            for valute in tree.findall('Valute'):
                if valute.find('CharCode').text == 'USD':
                    return float(valute.find('Value').text.replace(',', '.'))
        return None

    # Чтение существующего файла с курсами
    if os.path.exists(currency_file):
        with open(currency_file, 'r') as f:
            existing_data = f.readlines()
        existing_dates = {line.split(',')[0] for line in existing_data}
    else:
        existing_data = []
        existing_dates = set()

    # Обработка входного списка и дополнение данными курса ЦБ
    updated_data = []
    for date_str, rate in dates_and_rates:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        if date >= datetime.now().date():
            continue
        if date_str not in existing_dates:
            cbr_rate = get_cbr_rate(date)
            if cbr_rate is not None:
                diff = 'nan' if rate == 'nan' else f'{float(rate) - cbr_rate:.2f}'
                updated_data.append(f'{date_str},{rate},{cbr_rate},{diff}\n')

    # Запись обновленных данных в файл
    with open(currency_file, 'a') as f:
        f.writelines(updated_data)

# Чтение данных из файла конфигурации для экспорта сообщений
config = ConfigParser()
config.read('config.ini')

api_id = config.getint('telegram', 'api_id')
api_hash = config.get('telegram', 'api_hash')
phone = config.get('telegram', 'phone')
session_name = config.get('telegram', 'session_name')

# Создаем клиента для экспорта сообщений
client = TelegramClient(session_name, api_id, api_hash)

# Включаем логирование для экспорта сообщений
logging.basicConfig(level=logging.INFO)

def start_export():
    with client:
        client.loop.run_until_complete(export_main())
