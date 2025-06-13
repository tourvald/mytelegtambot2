import os
import json
import random
import unicodedata
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import GetHistoryRequest
import asyncio

# Введите ваши данные
api_id = 9389967          # Замените на ваш api_id
api_hash = 'a701b1d0675674c9ba7b5d05a76d15ae'    # Замените на ваш api_hash
phone_number = '+79263816112'  # В формате '+1234567890'
chat_id = 1573843884             # ID чата, который нужно мониторить


# Время задержки между проверками в секундах
polling_interval = 10

# Получаем директорию, где находится скрипт
script_dir = os.path.dirname(os.path.abspath(__file__))

# Файл для сохранения реакций (полный путь)
reactions_file = os.path.join(script_dir, 'reactions.json')

# Файл с ответами (полный путь)
messages_file = os.path.join(script_dir, 'messages.txt')

# Функция для загрузки сохранённых реакций из файла
def load_reactions():
    if os.path.exists(reactions_file):
        try:
            with open(reactions_file, 'r', encoding='utf-8') as file:
                reactions = json.load(file)
                return reactions
        except json.JSONDecodeError:
            return {}
    else:
        return {}

# Функция для сохранения реакций в файл
def save_reactions(reactions):
    with open(reactions_file, 'w', encoding='utf-8') as file:
        json.dump(reactions, file, ensure_ascii=False, indent=4)

# Функция для загрузки сообщений из файла messages.txt
def load_messages():
    if os.path.exists(messages_file):
        try:
            with open(messages_file, 'r', encoding='utf-8') as file:
                lines = [line.strip() for line in file if line.strip()]
                return lines
        except Exception as e:
            print(f"Ошибка при чтении файла messages.txt: {e}")
            return []
    else:
        print("Файл messages.txt не найден.")
        return []

async def main():
    client = TelegramClient('session_name', api_id, api_hash)
    await client.start()

    if not await client.is_user_authorized():
        try:
            await client.send_code_request(phone_number)
            code = input('Введите код, отправленный вам в Telegram: ')
            await client.sign_in(phone_number, code)
        except SessionPasswordNeededError:
            password = input('Введите пароль двухфакторной аутентификации: ')
            await client.sign_in(password=password)

    print(f"Мониторинг реакций на ваши сообщения в чате с ID: {chat_id}")

    # Получаем информацию о текущем пользователе
    me = await client.get_me()
    my_user_id = me.id

    # Загружаем предыдущие реакции из файла
    previous_reactions = load_reactions()

    # Загружаем ответы из файла messages.txt
    messages_list = load_messages()
    if not messages_list:
        print("Список ответов пуст. Убедитесь, что файл messages.txt содержит хотя бы одну строку.")
        return

    while True:
        try:
            # Получаем последние 100 сообщений из чата
            history = await client(GetHistoryRequest(
                peer=chat_id,
                offset_id=0,
                offset_date=None,
                add_offset=0,
                limit=100,
                max_id=0,
                min_id=0,
                hash=0
            ))

            # Фильтруем только свои последние 10 сообщений
            my_messages = [msg for msg in history.messages if msg.sender_id == my_user_id][:10]

            for message in my_messages:
                message_id = str(message.id)

                if message.reactions:
                    # Извлекаем упрощенную структуру реакций
                    reactions = {}
                    for reaction in message.reactions.results:
                        if hasattr(reaction.reaction, 'emoticon'):
                            emoji = reaction.reaction.emoticon
                        else:
                            emoji = 'unknown'

                        reactions[emoji] = reaction.count

                    # Получаем предыдущие реакции на это сообщение
                    prev_reactions = previous_reactions.get(message_id, {})

                    # Проверяем, есть ли новые или увеличенные реакции
                    for emoji, count in reactions.items():
                        prev_count = prev_reactions.get(emoji, 0)
                        if count > prev_count:
                            # Нормализуем эмодзи для сравнения
                            emoji_normalized = unicodedata.normalize('NFKD', emoji)
                            if emoji_normalized == '🤡':
                                # Выбираем случайную строку из messages_list
                                random_message = random.choice(messages_list)
                                print(f"{random_message}")
                            else:
                                print(f"На ваше сообщение с ID {message_id} добавлена реакция '{emoji}': всего {count}")

                    # Обновляем реакции в предыдущих данных
                    previous_reactions[message_id] = reactions

                else:
                    # Если на сообщение нет реакций, но ранее были, удаляем запись
                    if message_id in previous_reactions:
                        del previous_reactions[message_id]

            # Сохраняем обновленные реакции в файл
            save_reactions(previous_reactions)

        except Exception as e:
            print(f"Ошибка: {e}")

        # Ожидание перед следующим опросом
        await asyncio.sleep(polling_interval)

if __name__ == '__main__':
    asyncio.run(main())