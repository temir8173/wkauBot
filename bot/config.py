import os

from sqlalchemy.engine import URL


# load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
SCHEDULE_API_BASE_URL = os.getenv("SCHEDULE_API_URL")
SCHEDULE_API_OPTIONS_URL = os.getenv("SCHEDULE_API_URL") + '/options'
SCHEDULE_API_SCHEDULE_URL = os.getenv("SCHEDULE_API_URL") + '/schedule'
REDIS_HOST = 'telegram-cache'
POSTGRES_HOST = 'telegram-db'

if not os.getenv('POSTGRES_USER'):
    from bot.db import setup_env
    setup_env()
    POSTGRES_HOST = 'localhost'
    REDIS_HOST = 'localhost'

redis_credentials = {
    'host': REDIS_HOST,
    'password': os.getenv("REDIS_PASSWORD"),
}
postgres_credentials = {
    'username': os.getenv("POSTGRES_USER"),
    'host': POSTGRES_HOST,
    'database': os.getenv("POSTGRES_DB"),
    'port': os.getenv("POSTGRES_PORT") or 5432,
    'password': os.getenv("POSTGRES_PASSWORD"),
}
SQLALCHEMY_DB_URI = URL.create(
    "postgresql+pg8000",
    **postgres_credentials
)
SQLALCHEMY_ASYNC_DB_URI = URL.create(
    "postgresql+asyncpg",
    **postgres_credentials
)
SQLALCHEMY_ECHO = True

open("test.txt", "a").__exit__()