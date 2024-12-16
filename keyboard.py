from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton

teams = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text="1", callback_data="team:1"),
    InlineKeyboardButton(text="2", callback_data="team:2"),
    InlineKeyboardButton(text="3", callback_data="team:3"),
    InlineKeyboardButton(text="4", callback_data="team:4"),
    InlineKeyboardButton(text="5", callback_data="team:5")
]])