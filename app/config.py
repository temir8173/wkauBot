import os
# from dotenv import load_dotenv

# load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

open("test.txt", "a").__exit__()