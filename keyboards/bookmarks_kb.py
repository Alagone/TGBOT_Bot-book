from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import data
from services.logger import logger
from services.file_handling import book

def generate_keyboard_of_bookmarks(bookmarks: list[int], additional_buttons: list[str]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    logger.info("Клавиатура закладок состоит из:\n"
                f"--отдельных кнопок: {', '.join(additional_buttons)}\n"
                f"--закладок: {', '.join([str(bookmark) for bookmark in bookmarks])}")
    for bookmark in bookmarks:
        builder.row(InlineKeyboardButton(text=f'{str(bookmark)} - {book[bookmark]}', callback_data=f'open_the_bookmark {bookmark}'))
    builder.row(*[InlineKeyboardButton(text=data[button] if button in data else button, callback_data=button) for button in additional_buttons])
    return builder.as_markup()

def generate_keyboard_of_editable_bookmarks(bookmarks: list[int], additional_buttons: list[str]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for bookmark in bookmarks:
        if bookmark == "page":#############
            print(bookmarks)
            print(123456)
        builder.row(InlineKeyboardButton(text=f'❌{str(bookmark)} - {book[bookmark]}', callback_data=f'delete_the_bookmark {bookmark}'))
    builder.row(
        *[InlineKeyboardButton(text=data[button] if button in data else button, callback_data=button) for button in
          additional_buttons])
    return builder.as_markup()