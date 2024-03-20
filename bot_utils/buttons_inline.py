from aiogram import types


btn_subscribe = types.InlineKeyboardButton(
    text='Подписаться',
    callback_data='subscribe_unsubscribe'
)

kb_sub = types.InlineKeyboardMarkup(
    inline_keyboard=[[btn_subscribe]]
)


btn_unsubscribe = types.InlineKeyboardButton(
    text='Остановить уведомления',
    callback_data='subscribe_unsubscribe'
)

kb_unsub = types.InlineKeyboardMarkup(
    inline_keyboard=[[btn_unsubscribe]]
)
