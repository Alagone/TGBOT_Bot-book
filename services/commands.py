from aiogram.types import BotCommand
from lexicon.lexicon import LEXICON_COMMANDS

async def set_default_menu_of_commands(logger, bot, set = False):
    if not set:
        return
    logger.info("Bot is editing the menu of commands")
    await bot.set_my_commands(
        [
            BotCommand(command=key, description=value)
            for key, value in LEXICON_COMMANDS.items()
        ]
    )