# import asyncio
# from os import environ

# from aiogram import Bot
# from app.bot_utils.config_logger import logging
# from app.handlers import dp
# from app.bot_utils.commands import bot_commands

# dev
import asyncio
from os import environ

from aiogram import Bot
from bot_utils.config_logger import logging
from handlers import dp
from bot_utils.commands import bot_commands

BOT_TOKEN = environ["BOT_TOKEN"]
with open('./bot_utils/bot_static/description.txt', 'r') as f:
    text_description = f.read()


async def main() -> None:
    bot = Bot(BOT_TOKEN)
    await bot.set_my_description(text_description)
    await bot.set_my_commands(bot_commands)
    await dp.start_polling(bot)


if __name__ == "__main__":
    print('run bot ...')  #
    logging
    asyncio.run(main())
