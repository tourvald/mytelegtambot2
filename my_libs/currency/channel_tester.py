from configparser import ConfigParser
import os
from telethon import TelegramClient


def _get_client():
    """Create TelegramClient using credentials from config.ini."""
    config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
    config = ConfigParser()
    config.read(config_path)
    api_id = config.getint('telegram', 'api_id')
    api_hash = config.get('telegram', 'api_hash')
    session_name = config.get('telegram', 'session_name')
    return TelegramClient(session_name, api_id, api_hash)


async def test_channel_by_id(channel_id: int):
    """Return channel info and last 5 messages for the given channel ID."""
    async with _get_client() as client:
        entity = await client.get_entity(channel_id)
        messages = []
        async for message in client.iter_messages(entity, limit=5):
            messages.append(message.message or '')
        return entity.to_dict(), messages


async def test_channel_by_username(username: str):
    """Return channel info and last 5 messages for the given @username."""
    if not username.startswith('@'):
        username = '@' + username
    async with _get_client() as client:
        entity = await client.get_entity(username)
        messages = []
        async for message in client.iter_messages(entity, limit=5):
            messages.append(message.message or '')
        return entity.to_dict(), messages
