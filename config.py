import os
from dotenv import load_dotenv
from pathlib import Path
import platform

BASE_DIR = Path(__file__).resolve().parent
PRIVATE_DIR = BASE_DIR / 'private_data'

# Load environment variables from the optional private directory
load_dotenv(PRIVATE_DIR / '.env')

# Ensure that at least one bot token is provided
if not (os.getenv('BOT_TOKEN') or os.getenv('BOT_TOKEN_WIN')):
    raise RuntimeError('BOT_TOKEN not configured')

if platform.processor() == 'Intel64 Family 6 Model 42 Stepping 7, GenuineIntel':
    BOT_TOKEN = os.getenv("BOT_TOKEN_WIN")
else:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
