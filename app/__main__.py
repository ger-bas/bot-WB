import asyncio
from os import environ

from aiogram import Bot

from bot_utils.config_logger import logging
from handlers import dp

BOT_TOKEN = environ["BOT_TOKEN"]


async def main() -> None:
    bot = Bot(BOT_TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging
    print('bot run...')
    asyncio.run(main())
