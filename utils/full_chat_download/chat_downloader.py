from telethon import TelegramClient
import os
from data.config import API_ID, API_HASH  # Ensure your config has these
from datetime import datetime

async def download_chat_history(target_id: int, session_id: int):
    """
    Downloads the full chat history and media for a given target_id
    using the session ID of a previously authorized user.

    Args:
        target_id (int): The Telegram ID of the user whose chat history to download.
        session_id (int): The session ID (numeric part of the .session filename, no extension).
    """
    session_folder = "mysessya"
    session_name = str(session_id)  # Do NOT add `.session` extension here
    session_path = os.path.join(session_folder, session_name)

    # Check if the session file exists
    if not os.path.exists(session_path + ".session"):
        print(f"❌ Session file not found: {session_path}.session")
        return False

    print(f"📦 Starting chat download from target ID: {target_id} using session: {session_name}")

    # Prepare download folder
    download_folder_name = f"full_chat_download_{target_id}_{session_name}"
    download_folder_path = os.path.join("downloads", download_folder_name)
    os.makedirs(download_folder_path, exist_ok=True)

    log_file_path = os.path.join(download_folder_path, "full_chat_history.txt")

    # Initialize Telegram client
    client = TelegramClient(session_path, API_ID, API_HASH)

    try:
        await client.connect()
        if not await client.is_user_authorized():
            print(f"⚠️ Unauthorized session: {session_name}")
            return False

        entity = await client.get_entity(target_id)
        print(f"🧾 Downloading chat with: {getattr(entity, 'username', None) or entity.first_name}")

        with open(log_file_path, "w", encoding="utf-8") as log:
            async for msg in client.iter_messages(entity, reverse=True):
                timestamp = msg.date.strftime("%Y-%m-%d %H:%M:%S") if msg.date else "Unknown Time"
                sender = await msg.get_sender()
                name = getattr(sender, 'first_name', 'Unknown')
                sender_id = getattr(sender, 'id', 'Unknown ID')

                if msg.text:
                    log.write(f"[{timestamp}] {name} ({sender_id}): {msg.text}\n")
                elif msg.media:
                    try:
                        filename = await msg.download_media(file=download_folder_path)
                        log.write(f"[{timestamp}] {name} ({sender_id}) sent media: {os.path.basename(filename)}\n")
                    except Exception as media_err:
                        log.write(f"[{timestamp}] {name} ({sender_id}) sent media but failed to download: {media_err}\n")
                else:
                    log.write(f"[{timestamp}] {name} ({sender_id}) sent unknown message type\n")

        print(f"✅ Chat history and media saved to: {download_folder_path}")
        return download_folder_path

    except Exception as e:
        print(f"❌ Error during chat download: {e}")
        return False

    finally:
        await client.disconnect()


from PIL import Image, ImageDraw, ImageFont

def generate_code_image(code_text: str, save_path: str = "code.png"):
    width, height = 600, 200
    background_color = (255, 255, 255)
    text_color = (30, 30, 30)

    img = Image.new('RGB', (width, height), color=background_color)
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()

    text = f"Telegram Confirmation Code:\n\n{code_text}"
    draw.multiline_text((50, 50), text, fill=text_color, font=font, spacing=10)

    img.save(save_path)
    return save_path
