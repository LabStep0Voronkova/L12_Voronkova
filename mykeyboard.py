from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# Главная клавиатура
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Узнать погоду")],
        [KeyboardButton(text="Регистрация")]
    ],
    resize_keyboard=True
)

# Клавиатура выбора пола
gender_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Мужской")],
        [KeyboardButton(text="Женский")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

# Клавиатура времени (часы)
def time_hours_keyboard():
    buttons = []
    row = []
    for h in range(0, 24):
        row.append(InlineKeyboardButton(text=str(h), callback_data=f"hour_{h}"))
        if len(row) == 4:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# Клавиатура времени (минуты)
def time_minutes_keyboard():
    buttons = []
    row = []
    for m in range(0, 60, 5):
        row.append(InlineKeyboardButton(text=str(m), callback_data=f"minute_{m}"))
        if len(row) == 6:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# Клавиатура частоты уведомлений
freq_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="ежедневно")],
        [KeyboardButton(text="еженедельно")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)