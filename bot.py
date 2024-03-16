# flake8:noqa
import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from dotenv import load_dotenv

from data_base.get_wb import get_product_wb
from data_base.use_db import get_or_add_product

# import my_requests.get_wb as g_wb
# get_product_wb = g_wb.get_product_wb()

load_dotenv()

# Bot token can be obtained via https://t.me/BotFather
TOKEN = getenv("BOT_TOKEN")

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    hello = f'Hello, {hbold(message.from_user.full_name)}!\n'
    hello_message = ('Пришли мне артикул товара с площадки Wildberries '
                     'и я покажу тебе информацию о нём.')
    await message.answer(hello + hello_message)


@dp.message()
async def echo_handler(message: types.Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    try:
        # Send a copy of the received message
        # await message.send_copy(chat_id=message.chat.id)
        if not message.text.isdigit():
            await message.answer('артикул может состоять только из цифр')
        elif len(message.text) > 20:
            await message.answer('артикул более 20 символов')
        else:
            product = get_or_add_product(message.text, message.chat.id)
            # product = get_product_wb(message.text)
            print(product)
            if product:
                output_message = (
                    f'Название:   {product.name}\n'
                    f'Артикул:   {product.vendor_code}\n'
                    f'Цена:   {product.price}\n'
                    f'Рейтинг:   {product.rating}\n'
                    f'Количество:   {product.quantity}'
                )
            else:
                output_message = 'Информация отсутствует, проверь артикул.'
            await message.answer(output_message)
    except Exception as e:
        print(e)
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        # Но не все типы поддерживаются для копирования, поэтому необходимо с этим справиться.
        await message.answer("Nice try!")


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())


# /home/ger/Dev/bot-WB/bot/bot.py
