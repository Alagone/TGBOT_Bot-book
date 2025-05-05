from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from decouple import config

import asyncio

from handlers.particular_handlers import book_router
from services.logger import logger
from handlers.default_handlers import default_router
from services.commands import set_default_menu_of_commands

async def main():
    bot = Bot(config("TOKEN"), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers(default_router, book_router)
    await set_default_menu_of_commands(logger, bot, True)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())