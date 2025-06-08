from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, FSInputFile, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.keyboard import InlineKeyboardBuilder
import asyncio
import requests
from config import BOT_TOKEN, WEATHER_API_KEY
from database import init_db, add_or_update_user, get_user, get_users
from mykeyboard import main_keyboard, gender_keyboard, freq_keyboard
from utils import is_admin, get_weather_image

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

class Registration(StatesGroup):
    gender = State()
    hour = State()
    minute = State()
    notification_freq = State()

@dp.message(CommandStart())
async def start(message: Message):
    if is_admin(message):
        admin_keyboard = main_keyboard
        admin_keyboard.keyboard.append([KeyboardButton(text="Пользователи")])
        await message.answer("Привет, администратор!", reply_markup=admin_keyboard)
    else:
        await message.answer("Привет!", reply_markup=main_keyboard)

@dp.message(F.text == "Узнать погоду")
async def get_weather(message: Message):
    url = f"https://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q=Moscow"
    response = requests.get(url)
    data = response.json()

    if "error" in data:
        await message.answer("Ошибка получения погоды.")
        return

    temp_c = data["current"]["temp_c"]
    image_path = get_weather_image(temp_c)
    photo = FSInputFile(image_path)
    await message.answer_photo(photo=photo, caption=f"Температура в Москве: {temp_c}°C")

@dp.message(F.text == "Регистрация")
async def registration_start(message: Message, state: FSMContext):
    await state.set_state(Registration.gender)
    await message.answer("Выберите ваш пол:", reply_markup=gender_keyboard)

@dp.message(Registration.gender)
async def registration_gender(message: Message, state: FSMContext):
    await state.update_data(gender=message.text)
    await state.set_state(Registration.hour)
    await message.answer("Выберите час для уведомлений:", reply_markup=time_hours_keyboard())

@dp.callback_query(Registration.hour)
async def registration_hour(callback: CallbackQuery, state: FSMContext):
    hour = callback.data.split("_")[1]
    await state.update_data(hour=hour)
    await state.set_state(Registration.minute)
    await callback.message.edit_text("Выберите минуты для уведомлений:", reply_markup=time_minutes_keyboard())

@dp.callback_query(Registration.minute)
async def registration_minute(callback: CallbackQuery, state: FSMContext):
    minute = callback.data.split("_")[1]
    await state.update_data(minute=minute)
    await state.set_state(Registration.notification_freq)
    await callback.message.edit_text("Выберите частоту уведомлений:", reply_markup=freq_keyboard)

@dp.message(Registration.notification_freq)
async def registration_notification_freq(message: Message, state: FSMContext):
    data = await state.get_data()
    user_data = {
        "telegram_id": message.from_user.id,
        "username": message.from_user.username,
        "gender": data["gender"],
        "notification_time": f"{data['hour']}:{data['minute']}",
        "notification_freq": message.text
    }
    await add_or_update_user(**user_data)
    await message.answer("Вы успешно зарегистрированы!")
    await state.clear()

@dp.message(F.text == "Пользователи")
async def show_users(message: Message):
    if not is_admin(message):
        await message.answer("Нет доступа.")
        return

    users = await get_users()
    if not users:
        await message.answer("Пользователей нет.")
        return

    result = "Зарегистрированные пользователи:\n"
    for u in users:
        result += f"ID: {u[0]}, Имя: {u[1]}, Пол: {u[2]}, Время: {u[3]}, Частота: {u[4]}\n"
    await message.answer(result)

async def main():
    await init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())