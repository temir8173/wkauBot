import os

from sqlalchemy.engine import URL

# from dotenv import load_dotenv


if not os.getenv('POSTGRES_USER'):
    from bot.db import setup_env

    setup_env()


# load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
REDIS_HOST = 'telegram-cache'

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_HOST = 'localhost'
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_PORT = os.getenv("POSTGRES_PORT") or 5432
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")


SQLALCHEMY_DB_URI = URL.create(
    "postgresql+pg8000",
    username=POSTGRES_USER,
    host=POSTGRES_HOST,
    database=POSTGRES_DB,
    port=POSTGRES_PORT,
    password=POSTGRES_PASSWORD
)
SQLALCHEMY_ASYNC_DB_URI = URL.create(
    "postgresql+asyncpg",
    username=POSTGRES_USER,
    host=POSTGRES_HOST,
    database=POSTGRES_DB,
    port=POSTGRES_PORT,
    password=POSTGRES_PASSWORD
)
SQLALCHEMY_ECHO = True

open("test.txt", "a").__exit__()