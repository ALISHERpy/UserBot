from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.enums.parse_mode import ParseMode
from utils.shortcuts import safe_markdown

router = Router()

@router.message(CommandStart())
async def do_start(message: types.Message):

    full_name = message.from_user.full_name
    msg = (
        "👋 Cheklangan kontent yuklash botiga xush kelibsiz\!\n\n"
        "✳️ Bir marta ko‘rinadigan postlarni saqlash\.\n"
        "✳️ Batafsil Qollanma uchun /qollanma ni bosing\.\n"
        # "✳️ Botdan tashqari \(do‘stdan\) media yuklash uchun media ostiga /ok yozing\.\n"
        # "⚠️ Kontent yuklashdan oldin albatta /login bilan tizimga kiring\!\n"
        "✳️ Batafsil ma’lumot uchun /help ni bosing\."
    )
    # msg= "\nBot remontda,xavfsizlik kuchaytirilmoqda \n\n9 uyun kuni soat 10:00gacha \n\nqayta ishlaydi\nIltimos sabr qilamiz"
    await message.answer(f"Assalomu alaykum {safe_markdown(full_name)}\!\n {msg}", parse_mode=ParseMode.MARKDOWN_V2)

    # text = "https://t.me/take_image/4"
    # await message.answer(text=text)
