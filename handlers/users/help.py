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

@router.message(Command('qollanma'))
async def qollanma(message: types.Message):
    text = "https://t.me/take_image/4"
    await message.answer(text=text)
    text = """🔐 1. Tizimga kirish
Botdan foydalanish uchun avval tizimga kiring:
📌 Buyruq yuboring: /login
📲 Keyin:
📱 Raqamingizni yuboring.
🔢 Telegramdan kelgan 5 xonali kodni kiriting.
🔒 Agar parol (2FA) o‘rnatilgan bo‘lsa, uni ham kiriting.
✅ Shu bilan botga kirish tugaydi.

💾 2. Bir marlatik faylni saqlash.
Agar sizga Do'stinggizdan faqat bir marta ko‘rinadigan fayl kelsa (rasm/video):
🗨 O‘sha faylga javoban /ok yozing:
Bot sizga uni yuklab yuboradi ✅

🚪 3. Tizimdan chiqish
Botdan chiqmoqchimisiz?
Yuboring:
/logout
Sizning sessiyangiz yopiladi va botdan chiqasiz.
    """
    await message.answer(text=text)
    text="""
    ⚠️ DIQQAT!
Quyidagi holatlarda botdan foydalanmang:

☎️ Agar sizning Telegram raqamingiz noaktiv bo‘lsa (ya’ni, SIM-kartangiz hozir sizda bo‘lmasa, eski raqam bo‘lsa).

🌍 Agar siz chet el raqamiga ochilgan Telegram hisobidan foydalansangiz.

❓ Nega?
Bu Telegram’ning rasmiy xavfsizlik siyosatiga bog‘liq. Yuqoridagi 2 turdagi akkauntlar bilan ishlaganda ba’zi texnik muammolar yuzaga kelishi mumkin, bu esa botimizning to‘liq ishlashiga xalaqit beradi.
👨‍🦳Admin : @take_image"""
    await message.answer(text=text)
