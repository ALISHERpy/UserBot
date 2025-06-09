from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.session.middlewares.request_logging import logger
from loader import db, bot
from data.config import ADMINS
from utils.shortcuts import safe_markdown

router = Router()


@router.message(CommandStart())
async def do_start(message: types.Message):
    """
            MARKDOWN V2                     |     HTML
    link:   [Google](https://google.com/)   |     <a href='https://google.com/'>Google</a>
    bold:   *Qalin text*                    |     <b>Qalin text</b>
    italic: _Yotiq shriftdagi text_         |     <i>Yotiq shriftdagi text</i>



                    **************     Note     **************
    Markdownda _ * [ ] ( ) ~ ` > # + - = | { } . ! belgilari to'g'ridan to'g'ri ishlatilmaydi!!!
    Bu belgilarni ishlatish uchun oldidan \ qo'yish esdan chiqmasin. Masalan  \.  ko'rinishi . belgisini ishlatish uchun yozilgan.
    """

    telegram_id = message.from_user.id
    full_name = message.from_user.full_name
    username = message.from_user.username
    user = None
    try:
        user = await db.add_user(telegram_id=telegram_id, full_name=full_name, username=username)
    except Exception as error:
        logger.info(error)
    if user:
        count = await db.count_users()
        msg = (f"[{safe_markdown(user['full_name'])}](tg://user?id={user['telegram_id']}) bazaga qo'shildi\.\nBazada {count} ta foydalanuvchi bor\.")
    else:
        msg = f"[{safe_markdown(full_name)}](tg://user?id={telegram_id}) bazaga oldin qo'shilgan"
    for admin in ADMINS:
        try:
            await bot.send_message(
                chat_id=admin,
                text=msg,
                parse_mode=ParseMode.MARKDOWN_V2
            )
        except Exception as error:
            logger.info(f"Data did not send to admin: {admin}. Error: {error}")

    msg = (
        "👋 Cheklangan kontent yuklash botiga xush kelibsiz\!\n\n"
        "✳️ Bir marta ko‘rinadigan postlarni saqlash\.\n"
        "✳️ Batafsil Qollanma uchun /qollanma ni bosing\.\n"
        "✳️ Botdan tashqari \(do‘stdan\) media yuklash uchun media ostiga /ok yozing\.\n"
        "⚠️ Kontent yuklashdan oldin albatta /login bilan tizimga kiring\!\n"
        "✳️ Batafsil ma’lumot uchun /help ni bosing\."
    )
    # msg= "\nBot remontda,xavfsizlik kuchaytirilmoqda \n\n9 uyun kuni soat 10:00gacha \n\nqayta ishlaydi\nIltimos sabr qilamiz"

    await message.answer(f"Assalomu alaykum {safe_markdown(full_name)}\!\n {msg}", parse_mode=ParseMode.MARKDOWN_V2)

