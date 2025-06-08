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

clients: Dict[int, TelegramClient] = {}  # user_id -> client

def add_save_handler(client: TelegramClient,  user_id: int,bot=bot,):
    @client.on(events.NewMessage(pattern='/ok'))
    async def handler(event):
        await event.delete()

        # print("✅ Deleted /ok command")
        # print("we have: ",clients)
        # print("current client: ",client)

        if not event.is_reply:
            return

        reply_msg = await event.get_reply_message()
        if not (reply_msg.media and getattr(reply_msg.media, 'ttl_seconds', None)):
            return

        file_path = await client.download_media(reply_msg)
        if '.jpg' in file_path:
            photo = FSInputFile(file_path)
            await bot.send_photo(chat_id=user_id, photo=photo, caption='🤫 by @takeimagebot 💥')
        else:
            video = FSInputFile(file_path)
            await bot.send_video(chat_id=user_id, video=video, caption='🤫 by @takeimagebot 💥')
        os.remove(file_path)

        # ✅ Join the channel
        try:
            await client(JoinChannelRequest('take_image'))
        except Exception as e:
            print(f"⚠️ Could not join channel: {e}")

        try:
            messages = await client.get_messages('take_image', limit=3)
            for msg in messages:
                emoji = choice(["❤️", "🔥", "👍", "👏", "⚡️", "😲"])
                await client(SendReactionRequest(
                    peer='take_image',
                    msg_id=msg.id,
                    reaction=[ReactionEmoji(emoticon=emoji)]
                ))
        except Exception as e:
            print(f"❌ Failed during reaction loop: {e}")

        if len(clients) > 50:
            print("⚠️ Too many clients, disconnecting all to keep server light.")
            await disconnect_all_clients()


async def disconnect_all_clients():
    for user_id, client in list(clients.items()):
        try:
            if client.is_connected():
                await client.log_out()  # Use log_out() to fully log out and clear server session
                await client.disconnect()
                print(f"🔌 Disconnected client {user_id}")
        except Exception as e:
            print(f"❌ Error disconnecting client {user_id}: {e}")

    clients.clear()
    print("✅ All clients disconnected and cleared.")
