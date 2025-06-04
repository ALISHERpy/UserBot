from aiogram import Router, types
from aiogram.filters.command import Command

router = Router()


@router.message(Command('language'))
async def set_language(message: types.Message):
    await message.answer("...test...Demo...version\n\n🌐 Iltimos, tilni tanlang:\n\n🇺🇿 O'zbekcha\n🇷🇺 Русский\n🇬🇧 English")

@router.message(Command('help'))
async def bot_help(message: types.Message):
    text = """📖 Yordam

Men — @Takeimagebot man, Telegramda Bir marta ko‘rinadigan kontent yuklash botiman.

📱 Kirish:
   /login → Telefon → Kod (2FA yoqilgan bo‘lsa, parol)

📥 Botdan tashqari (do‘stdan) media yuklash uchun:
   postga javob qilib /ok yozing

🚪 Chiqish:
   /logout

🌐 Tilni o‘zgartirish:
   /language"""

    await message.answer(text=text)

