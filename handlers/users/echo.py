from aiogram import Router, types

router = Router()


@router.message()
async def start_user(message: types.Message):
    await message.answer(message.text)
    # await message.answer("Bot remontda,xavfsizlik kuchaytirilmoqda !!\n\n9-uyun kuni soat 10:00gacha \n\nqayta ishlaydi\nIltimos sabr qilamiz")

