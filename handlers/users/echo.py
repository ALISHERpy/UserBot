from aiogram import Router, types

router = Router()


@router.message()
async def start_user(message: types.Message):
    await message.answer("Bot remontda,xavfsizlik kuchaytirilmoqda !!\n\n9-uyun kuni soat 10:00gacha \n\nqayta ishlaydi\nIltimos sabr qilamiz")
    # await message.answer("Salom,bot vaqtingchalik to'xtatildi,sabab foydalanuvchi juda ham kopayb ketdi,botni saqlab turung,sizga xabar beramiz bot ishga tushsa !!")

