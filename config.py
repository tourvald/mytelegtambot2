import os
from dotenv import load_dotenv
import platform
load_dotenv()
print (platform.processor())
if platform.processor() == 'Intel64 Family 6 Model 42 Stepping 7, GenuineIntel':
	BOT_TOKEN = os.getenv("BOT_TOKEN_WIN")
else:
	BOT_TOKEN = os.getenv("BOT_TOKEN")