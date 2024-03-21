from os import environ, getenv

from dotenv import load_dotenv

load_dotenv()

environ['BOT_TOKEN'] = getenv('BOT_TOKEN')
environ['POSTGRES_LOGIN'] = getenv('POSTGRES_LOGIN')
environ['POSTGRES_PASSWORD'] = getenv('POSTGRES_PASSWORD')
