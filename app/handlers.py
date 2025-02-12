# import asyncio

# from aiogram import Dispatcher, F, types
# from aiogram.filters import Command
# from aiogram.enums import ParseMode

# from app.bot_utils.buttons import keyboard
# from app.bot_utils.buttons_inline import kb_sub, kb_unsub
# from app.bot_utils.config_logger import logging
# from app.bot_utils.secondary_funcs import check_subscribe, find_vendor_code
# from app.data_base.use_db import get_or_add_product, last_five_entries

# dev
import asyncio

from aiogram import Dispatcher, F, types
from aiogram.filters import Command
from aiogram.enums import ParseMode

from bot_utils.buttons import keyboard
from bot_utils.buttons_inline import kb_sub, kb_unsub
from bot_utils.config_logger import logging
from bot_utils.secondary_funcs import check_subscribe, find_vendor_code
from data_base.use_db import get_or_add_product, last_five_entries

dp = Dispatcher()
TIME_OUT = 60 * 5


@dp.message(Command('start'))
async def command_start_handler(message: types.Message) -> None:
    """Reaction to the "/start" command."""
    hello = f'Привет, {message.from_user.full_name}!\n'
    hello_message = ('Пришли мне артикул товара с площадки Wildberries '
                     'и я покажу тебе информацию о нём.')
    await message.answer(hello + hello_message, reply_markup=keyboard)


@dp.message(Command('help'))
async def command_help_handler(message: types.Message) -> None:
    """Reaction to the "/help" command."""
    with open('./bot_utils/bot_static/help_text.txt', 'r') as f:
        help_text = f.read()
    await message.answer(help_text, parse_mode=ParseMode.MARKDOWN)


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
    vendor_code = find_vendor_code(message.text)
    text_up = (
        'Вы подписались на получение уведомлений со следущим текстом:\n\n'
    )
    product_data = get_or_add_product(vendor_code)
    text_after = (
        ('\n\nУведомления будут приходить каждые 5 минут.\n'
         'Для отключения уведомлений воспользуйтесь кнопкой '
         '"Остановить уведомления"')
    )
    full_text = text_up + product_data + text_after
    await message.answer(full_text, reply_markup=kb_unsub)
    while True:
        await asyncio.sleep(TIME_OUT)
        await message.answer(
            get_or_add_product(vendor_code), reply_markup=kb_unsub
        )


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
            logging.info({'subscribe': {
                'user': chat_id,
                'vendor_code': find_vendor_code(callback.message.text),
                }
            })
            await asyncio.sleep(0.1)
    if button_text == 'Остановить уведомления':
        if task:
            task.cancel()
            logging.info({'unsubscribe': {
                'user': chat_id,
                'vendor_code': find_vendor_code(callback.message.text),
                }
            })
            await callback.answer('Подписка отключена')
            message = callback.message
            await message.answer('Подписка отключена')
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
            product = get_or_add_product(message.text)
            if product:
                if check_subscribe(str(message.chat.id)):
                    await message.answer(product)
                else:
                    await message.answer(product, reply_markup=kb_sub)
            else:
                await message.answer(
                    'Информация отсутствует, проверьте артикул.'
                )
    except Exception as e:
        logging.exception(e)
