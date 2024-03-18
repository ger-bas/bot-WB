from aiogram import types


buttons = [
    [types.KeyboardButton(text='получить информацию из БД')],
]

keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
