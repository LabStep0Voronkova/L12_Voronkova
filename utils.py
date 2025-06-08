from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import ADMIN_ID
from mykeyboard import time_hours_keyboard, time_minutes_keyboard

# Проверка, является ли пользователь администратором
def is_admin(message: Message) -> bool:
    return message.from_user.id == ADMIN_ID

# Получение смайлика по температуре
def get_weather_image(temp_c):
    if temp_c < 0:
        return "assets/cold.png"
    elif 0 <= temp_c < 15:
        return "assets/cool.png"
    elif 15 <= temp_c < 25:
        return "assets/warm.png"
    else:
        return "assets/hot.png"