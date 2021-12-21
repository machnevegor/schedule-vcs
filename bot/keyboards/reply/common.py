from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

quick_keyboard = ReplyKeyboardBuilder().row(
    KeyboardButton(text="Звонки"),
    KeyboardButton(text="Уроки")
).as_markup(resize_keyboard=True)

days_keyboard = ReplyKeyboardBuilder().row(
    KeyboardButton(text="Понедельник"),
    KeyboardButton(text="Вторник"),
    KeyboardButton(text="Среда")
).row(
    KeyboardButton(text="Четверг"),
    KeyboardButton(text="Пятница"),
    KeyboardButton(text="Суббота")
).as_markup(resize_keyboard=True)
