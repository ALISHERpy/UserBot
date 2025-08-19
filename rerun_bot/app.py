import os
import asyncio
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message
from aiogram.filters import Command
from asyncio.subprocess import create_subprocess_shell, PIPE

# ---- Config ----
BOT_TOKEN = '8490351727:AAFkVL1bCz4FcpR7cjPeo2peWS8e7epDR6A'
# (optional) Restrict commands to your own Telegram user id for safety
ALLOWED_USER_ID = 6158127177 # put your numeric TG user id here or leave 0 to allow anyone

# screen / app settings
APP_DIR = "/home/ubuntu/bots/UserBot"
VENV_ACTIVATE = "/home/ubuntu/bots/UserBot/.venv/bin/activate"   # adjust if your venv path differs
SCREEN_OLD = "userbot"
SCREEN_NEW = "userbot"
APP_CMD = "python3 app.py"

router = Router()

def is_allowed(user_id: int) -> bool:
    return user_id == ALLOWED_USER_ID

async def run(cmd: str) -> tuple[int, str, str]:
    """Run a shell command and return (code, stdout, stderr)."""
    proc = await create_subprocess_shell(cmd, stdout=PIPE, stderr=PIPE)
    out, err = await proc.communicate()
    return proc.returncode, out.decode(errors="ignore"), err.decode(errors="ignore")

@router.message(Command("status"))
async def status(message: Message):
    if not is_allowed(message.from_user.id):
        return await message.answer("Access denied.")
    code, out, err = await run("screen -ls || true")
    text = f"Exit code: {code}\n\nSTDOUT:\n{out}\nSTDERR:\n{err}".strip()
    await message.answer(f"📟 *screen status:*\n```\n{text}\n```", parse_mode="Markdown")

@router.message(Command("stop_userbot"))
async def stop_userbot(message: Message):
    if not is_allowed(message.from_user.id):
        return await message.answer("Access denied.")
    cmd = f"screen -S {SCREEN_OLD} -X quit || true"
    code, out, err = await run(cmd)
    await message.answer(f"🛑 Killed `{SCREEN_OLD}` (if existed).\nExit code: {code}\n```\n{out}{err}\n```", parse_mode="Markdown")

@router.message(Command("restart_userbot"))
async def restart_userbot(message: Message):
    if not is_allowed(message.from_user.id):
        return await message.answer("Access denied.")

    await message.answer("⏳ Restarting…")

    # 1) kill old screen
    kill_cmd = f"screen -S {SCREEN_OLD} -X quit || true"
    code1, out1, err1 = await run(kill_cmd)

    # 2) ensure any stale new session is gone
    kill_new_cmd = f"screen -S {SCREEN_NEW} -X quit || true"
    code2, out2, err2 = await run(kill_new_cmd)

    # 3) start new screen with venv + app
    # Use bash -lc so 'source' works; cd into app dir first
    launch_cmd = (
        f"screen -dmS {SCREEN_NEW} bash -lc "
        f"\"cd {APP_DIR} && source {VENV_ACTIVATE} && {APP_CMD}\""
    )
    code3, out3, err3 = await run(launch_cmd)

    # 4) report
    report = (
        f"🧹 Kill `{SCREEN_OLD}` -> exit {code1}\n{(out1+err1).strip()}\n\n"
        f"🧹 Kill stale `{SCREEN_NEW}` -> exit {code2}\n{(out2+err2).strip()}\n\n"
        f"🚀 Start `{SCREEN_NEW}` -> exit {code3}\n{(out3+err3).strip()}"
    ).strip()

    await message.answer(f"✅ Done.\n```\n{report}\n```", parse_mode="Markdown")

async def main():
    bot = Bot(BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    print("Bot is running…")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
