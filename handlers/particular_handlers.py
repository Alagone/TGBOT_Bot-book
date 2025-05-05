from gc import callbacks
from typing import Tuple, Optional, Union

from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.methods import LogOut
from aiogram.types import Message, CallbackQuery
from pydantic.v1 import NotNoneError
from pyexpat.errors import messages

from lexicon.lexicon import data

from services.file_handling import book
from keyboards.poganation_kb import generate_keyboard_for_page
from keyboards.bookmarks_kb import generate_keyboard_of_bookmarks, generate_keyboard_of_editable_bookmarks
from datebase.datebase import users_db

book_router = Router()

msg_book_text: Message = None
msg_with_keyboard_of_bookmarks: Message = None
msg_with_keyboard_of_editable_bookmarks: Message = None

@book_router.message(Command("beginning"))
async def start_read_book_process(message: Message):
    global msg_book_text
    users_db[message.from_user.id]["page"] = 1
    msg_book_text = await message.answer(text=book[1], reply_markup=generate_keyboard_for_page("backward", f"{users_db[message.from_user.id]['page']}/{len(book)}", "forward"))

@book_router.message(Command("continue"))
async def continue_read_book_process(message: Message):
    global msg_book_text
    msg_book_text = await message.answer(text=book[users_db[message.from_user.id]["page"]], reply_markup=generate_keyboard_for_page("backward", f"{users_db[message.from_user.id]['page']}/{len(book)}", "forward"))

@book_router.callback_query(lambda call: call.data == "forward")
async def go_to_the_next_page_process(call: CallbackQuery):
    global msg_book_text
    user_number_of_page = users_db[call.from_user.id]["page"]
    if len(book) > user_number_of_page:
        user_number_of_page += 1
    else:
        await call.answer("Это последняя страница", show_alert=True)
        return
    users_db[call.from_user.id]["page"] = user_number_of_page
    await msg_book_text.edit_text(text=book[user_number_of_page], reply_markup=generate_keyboard_for_page("backward", f"{user_number_of_page}/{len(book)}", "forward"))

@book_router.callback_query(lambda call: call.data == "backward")
async def go_to_the_last_page_process(call: CallbackQuery):
    global msg_book_text
    user_number_of_page = users_db[call.from_user.id]["page"]
    if 1 < user_number_of_page:
        user_number_of_page -= 1
    else:
        await call.answer("Это первая страница", show_alert=True)
        return
    users_db[call.from_user.id]["page"] = user_number_of_page
    await msg_book_text.edit_text(text=book[user_number_of_page], reply_markup=generate_keyboard_for_page("backward", f"{user_number_of_page}/{len(book)}", "forward"))

@book_router.callback_query(lambda call: call.data == f"{users_db[call.from_user.id]['page']}/{len(book)}")
async def make_a_bookmark_process(call: CallbackQuery):
    users_db[call.from_user.id]["bookmarks"].add(users_db[call.from_user.id]["page"])

def divide_bookmark_call(call: CallbackQuery, keyword: str) -> str:
    if call.data.count(keyword) != 1:
        return "False"
    calldata: str = call.data
    calldata = calldata.strip()
    calldata = calldata.strip(f"{keyword} ")
    return calldata

@book_router.callback_query(lambda call: divide_bookmark_call(call, "open_the_bookmark").isdigit())
async def open_the_bookmark(call: CallbackQuery):
    global msg_book_text
    bookmark = int(divide_bookmark_call(call, "open_the_bookmark"))
    msg_book_text = await call.message.answer(text=book[bookmark], reply_markup=generate_keyboard_for_page("backward", f"{bookmark}/{len(book)}", "forward"))

@book_router.message(Command("bookmarks"))
async def view_bookmarks_process(message: Message):
    global msg_with_keyboard_of_bookmarks
    bookmarks = users_db[message.from_user.id]["bookmarks"]
    if bookmarks == set():
        await message.answer(data["warn_absense_of_bookmarks"])
        return
    msg_with_keyboard_of_bookmarks = await message.answer(data["bookmark_list_info"], reply_markup=generate_keyboard_of_bookmarks(bookmarks, ["edit_bookmark", "cancel_view_bookmark"]))

@book_router.callback_query(lambda call: call.data == "cancel_view_bookmark")
async def cancel_list_of_bookmark_process(call: CallbackQuery):
    global msg_with_keyboard_of_bookmarks
    if msg_with_keyboard_of_bookmarks != None:
        await msg_with_keyboard_of_bookmarks.delete()
        await call.message.answer(data["offer_continue_reading"])

@book_router.callback_query(lambda call: call.data == "edit_bookmark")
async def edit_bookmarks_process(call: CallbackQuery):
    global msg_with_keyboard_of_editable_bookmarks
    bookmarks = users_db[call.from_user.id]["bookmarks"]
    if bookmarks == set():
        await call.message.answer(data["warn_absense_of_bookmarks"])
        return
    msg_with_keyboard_of_editable_bookmarks = await call.message.answer(data["bookmark_edit_list_info"], reply_markup=generate_keyboard_of_editable_bookmarks(bookmarks, ["cancel_edit_bookmarks"]))

@book_router.callback_query(lambda call: divide_bookmark_call(call, "delete_the_bookmark").isdigit())
async def delete_the_bookmark_process(call: CallbackQuery):
    bookmark = int(divide_bookmark_call(call, "delete_the_bookmark"))
    users_db[call.from_user.id]["bookmarks"].remove(bookmark)
    if users_db[call.from_user.id]["bookmarks"] != set():
        await msg_with_keyboard_of_editable_bookmarks.edit_reply_markup(reply_markup=generate_keyboard_of_editable_bookmarks(users_db[call.from_user.id]["bookmarks"], ["cancel_edit_bookmarks"]))
    else:
        await call.message.answer(data["warn_absense_of_bookmarks"] + "\n\n" + data["offer_continue_reading"])
        await msg_with_keyboard_of_editable_bookmarks.delete()
        await msg_with_keyboard_of_bookmarks.delete()

@book_router.callback_query(lambda call: call.data == "cancel_edit_bookmarks")
async def cancel_editing_bookmarks_process(call: CallbackQuery):
    if msg_with_keyboard_of_bookmarks != None and msg_with_keyboard_of_editable_bookmarks != None:
        await msg_with_keyboard_of_bookmarks.delete()
        await msg_with_keyboard_of_editable_bookmarks.delete()
        await call.message.answer(data["offer_continue_reading"])

@book_router.message()
async def echo_process(message: Message):
    await message.reply(message.text)