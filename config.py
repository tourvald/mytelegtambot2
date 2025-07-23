import os
from dotenv import load_dotenv
from pathlib import Path
import platform

BASE_DIR = Path(__file__).resolve().parent
PRIVATE_DIR = BASE_DIR / 'private_data'

load_dotenv(PRIVATE_DIR / '.env')

if platform.processor() == 'Intel64 Family 6 Model 42 Stepping 7, GenuineIntel':
    BOT_TOKEN = os.getenv("BOT_TOKEN_WIN")
else:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
