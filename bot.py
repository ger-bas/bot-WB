import asyncio
from os import getenv

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from dotenv import load_dotenv

from bot_buttons.buttons import keyboard
from bot_buttons.buttons_inline import kb_sub, kb_unsub
from bot_utils import check_subscribe, find_article
from config_logger import logging
from data_base.use_db import get_or_add_product, last_five_entries

load_dotenv()
token = getenv("BOT_TOKEN")
dp = Dispatcher()
time_out = 60 * 5


@dp.message(Command('start'))
async def command_start_handler(message: types.Message) -> None:
    """Reaction to the "/start" command."""
    hello = f'Hello, {message.from_user.full_name}!\n'
    hello_message = ('Пришли мне артикул товара с площадки Wildberries '
                     'и я покажу тебе информацию о нём.')
    await message.answer(hello + hello_message, reply_markup=keyboard)


@dp.message(F.text.lower() == 'получить информацию из бд')
async def get_last_five_entries(message: types.Message) -> None:
    """Button response <получить информацию из БД>"""
    task = check_subscribe(str(message.chat.id))
    for product in last_five_entries():
        if task:
            await message.answer(product)
        else:
            await message.answer(product, reply_markup=kb_sub)


async def subscribe_process(message: types.Message) -> None:
    """Periodic sending of messages."""
    text_up = (
        'Вы подписались на получение уведомлений со следущим текстом:\n\n'
    )
    text_after = (
        ('\n\nУведомления будут приходить каждые 5 минут.\n'
         'Для отключения уведомлений воспользуйтесь кнопкой '
         '"Остановить уведомления"')
    )
    text = text_up + message.text + text_after
    await message.answer(text, reply_markup=kb_unsub)
    while True:
        await asyncio.sleep(time_out)
        await message.answer(message.text, reply_markup=kb_unsub)


@dp.callback_query(F.data == 'subscribe_unsubscribe')
async def subscribe_unsubscribe(callback: types.CallbackQuery) -> None:
    """Implements subscribe/unsubscribe functionality."""
    chat_id = str(callback.message.chat.id)
    button_text = callback.message.reply_markup.inline_keyboard[0][0].text
    task = check_subscribe(chat_id)

    if button_text == 'Подписаться':
        if task:
            await callback.answer('Доступна только одна подписка')
        else:
            await callback.answer('Подписка активирована')
            asyncio.create_task(
                subscribe_process(callback.message), name=chat_id,
            )
            logging.info({'activate': {
                'user': chat_id,
                'vendor_code': find_article(callback.message.text),
                }
            })
            await asyncio.sleep(0.1)
    if button_text == 'Остановить уведомления':
        if task:
            task.cancel()
            logging.info({'deactivate': {
                'user': chat_id,
                'vendor_code': find_article(callback.message.text),
                }
            })
            await callback.answer('Подписка отключена')
        else:
            await callback.answer('Нет активных подписок')


@dp.message()
async def my_handler(message: types.Message) -> None:
    """Reply to any message sent."""
    try:
        if len(message.text) > 20:
            await message.answer('Не более 20 символов')
        elif not message.text.isdigit():
            await message.answer('Артикул может состоять только из цифр')
        else:
            chat_id = str(message.chat.id)
            product = get_or_add_product(message.text, chat_id)
            if product:
                task = check_subscribe(chat_id)
                if task:
                    await message.answer(product)
                else:
                    await message.answer(product, reply_markup=kb_sub)
            else:
                await message.answer(
                    'Информация отсутствует, проверьте артикул.'
                )
    except Exception as e:
        logging.exception(e)


async def main() -> None:
    bot = Bot(token)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging
    print('bot run...')
    asyncio.run(main())
