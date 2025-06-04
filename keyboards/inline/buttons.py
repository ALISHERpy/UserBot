from aiogram.types import (InlineKeyboardMarkup,
                           InlineKeyboardButton,
                           ReplyKeyboardMarkup,
                           KeyboardButton)

inline_keyboard = [[
    InlineKeyboardButton(text="✅ Yes", callback_data='yes'),
    InlineKeyboardButton(text="❌ No", callback_data='no')
]]
are_you_sure_markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)




def generate_code_keyboard(code=""):
    digits = [str(i) for i in range(1, 10)]
    keyboard = [
        [InlineKeyboardButton(text=d, callback_data=f"digit:{code + d}") for d in digits[i:i+3]]
        for i in range(0, 9, 3)
    ]

    # Always show 0 and clear
    keyboard.append([
        InlineKeyboardButton(text="0", callback_data=f"digit:{code + '0'}"),
        InlineKeyboardButton(text="🗑 Tozalash", callback_data="clear")
    ])

    # Only show submit if length is 5
    if len(code) == 5:
        keyboard.append([
            InlineKeyboardButton(text="✅ Tasdiqlash", callback_data=f"submit:{code}")
        ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

number_button = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="📱 Raqamni yuborish", request_contact=True)]],
    resize_keyboard=True,
    one_time_keyboard=True
)

def format_code_display(code: str, length: int = 5) -> str:
    return " ".join(code + "_" * (length - len(code)))