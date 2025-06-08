from aiogram import Router, types

router = Router()


@router.message()
async def start_user(message: types.Message):
    await message.answer("Bot remontda,9may kuni soat 9:00dan 10:00gacha qayta ishlaydi")
    # await message.answer("Salom,bot vaqtingchalik to'xtatildi,sabab foydalanuvchi juda ham kopayb ketdi,botni saqlab turung,sizga xabar beramiz bot ishga tushsa !!")

