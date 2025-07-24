import os
from dotenv import load_dotenv
from pathlib import Path
import platform

BASE_DIR = Path(__file__).resolve().parent
PRIVATE_DIR = BASE_DIR / 'private_data'

# Load environment variables from the optional private directory
load_dotenv(PRIVATE_DIR / '.env')

bot_token = os.getenv('BOT_TOKEN')
bot_token_win = os.getenv('BOT_TOKEN_WIN')

# Ensure that at least one bot token is provided
if not (bot_token or bot_token_win):
    raise RuntimeError('BOT_TOKEN not configured')

if platform.processor() == 'Intel64 Family 6 Model 42 Stepping 7, GenuineIntel':
    BOT_TOKEN = bot_token_win or bot_token
else:
    BOT_TOKEN = bot_token or bot_token_win

if not BOT_TOKEN:
    raise RuntimeError('BOT_TOKEN not configured for this platform')
