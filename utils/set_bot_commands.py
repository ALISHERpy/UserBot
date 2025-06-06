from aiogram import Bot
from aiogram.methods.set_my_commands import BotCommand
from aiogram.types import BotCommandScopeAllPrivateChats


async def set_default_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Botni ishga tushirish"),
        BotCommand(command="/login", description="botdan ro'yxatdan o'tish"),
        BotCommand(command="/logout", description="Botdan chiqish"),
        BotCommand(command="/help", description="Yordam"),
    ]
    await bot.set_my_commands(commands=commands, scope=BotCommandScopeAllPrivateChats())
