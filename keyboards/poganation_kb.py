from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import data

def generate_keyboard_for_page(*buttons):
    builder = InlineKeyboardBuilder()
    builder.row(*[InlineKeyboardButton(text=data[button] if button in data else button, callback_data=button) for button in buttons])
    return builder.as_markup()