from aiogram import Dispatcher, Bot

from utils.config import BOT_TOKEN

dp = Dispatcher()
dp.include_router("routers.schedule:router")
dp.include_router("routers.student:router")

if __name__ == "__main__":
    bot = Bot(BOT_TOKEN, parse_mode="markdown")
    dp.run_polling(bot)
