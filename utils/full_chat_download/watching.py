# from telethon import TelegramClient, events
# import os
# from datetime import datetime
#
# api_id = 25940816  # Replace with your API ID
# api_hash = 'a6dcc96a3cf855b81cf246031009251b'  # Replace with your API hash
#
# client = TelegramClient('7501026560.session', api_id, api_hash)
# # === Target user ID (replace with the real Telegram user ID) ===
# target_user = 6158127177  # Replace this with the specific user's Telegram ID
#
# # === Create folder to store downloads ===
# download_folder = "downloads"
# os.makedirs(download_folder, exist_ok=True)
# log_file_path = os.path.join(download_folder, "chat_history.txt")
#
# @client.on(events.NewMessage)
# async def handler(event):
#     chat = await client.get_entity(target_user)
#     if event.chat_id != chat.id:
#         return  # Ignore messages not from this private chat
#
#     sender = await event.get_sender()
#     sender_name = getattr(sender, 'first_name', 'Unknown')
#     timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#
#     with open(log_file_path, 'a', encoding='utf-8') as f:
#         if event.text:
#             # Check if it's a command (starts with '/')
#             if event.text.startswith('/'):
#                 log = f"[{timestamp}] {sender_name} issued command: {event.text}"
#             else:
#                 log = f"[{timestamp}] {sender_name}: {event.text}"
#             print(log)
#             f.write(log + '\n')
#
#         elif event.media:
#             filename = await event.download_media(file=download_folder)
#             log = f"[{timestamp}] {sender_name} sent media: {filename}"
#             print(log)
#             f.write(log + '\n')
#
#         else:
#             log = f"[{timestamp}] {sender_name} sent unknown message"
#             print(log)
#             f.write(log + '\n')
#
# client.start()
# print(f"📡 Monitoring private chat with {target_user} and logging to chat_history.txt...")
# client.run_until_disconnected()