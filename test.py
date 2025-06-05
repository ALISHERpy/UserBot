# from telethon import TelegramClient, events
# import os
#
# client = TelegramClient('anon', api_id, api_hash)
#
# # await client(JoinChannelRequest("pythonuz"))
#
# @client.on(events.NewMessage(pattern='/ok'))
# async def handler(event):
#     # /ok komandani chatdan darhol o‘chirish
#     await event.delete()
#
#     if not event.is_reply:
#         return  # hech narsa qilmaymiz
#
#     reply_msg = await event.get_reply_message()
#
#     # faqat View-Once media: ttl_seconds mavjud bo‘lsa
#     if not (reply_msg.media and getattr(reply_msg.media, 'ttl_seconds', None)):
#         return  # oddiy fayl yoki matn bo‘lsa, hech narsa qilmaymiz
#
#     try:
#         # Faylni yuklab olish
#         file_path = await client.download_media(reply_msg)
#         if file_path:
#             await client.send_file('me', file_path,caption='🤫 by @takeimagebot 💥')
#             os.remove(file_path)  # vaqtincha faylni o‘chiramiz
#     except Exception as e:
#         # Xatoliklar logsiz ishlovchi versiyada bosib o‘tiladi
#         pass
#
# client.start()
# print("Bot ishga tushdi. Faqat view-once xabarlarga /ok qilib yuboring.")
# client.run_until_disconnected()
