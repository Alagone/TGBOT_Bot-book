from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from copy import deepcopy

from lexicon.lexicon import data
from datebase.datebase import users_db, user_dict_template

default_router = Router()

@default_router.message(CommandStart())
async def start_process(message: Message):
    await message.answer(data["start"])
    if message.from_user.id not in users_db:
        users_db[message.from_user.id] = deepcopy(user_dict_template)

@default_router.message(Command("help"))
async def help_process(message: Message):
    await message.reply(data["help"])