import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token="7039079899:AAGxogR1d0fEmZoD0pwjIL8p9QhgoubN3tM")
# Диспетчер
dp = Dispatcher()

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello!")

# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

# @dp.message(Command("start"))
# async def cmd_start(message: types.Message):
#     markup = types.InlineKeyboardMarkup()
#     markup.add(types.InlineKeyboardButton('Открыть MyGarage', web_app=types.WebAppInfo('https://ttestt.store/')))
#     await message.answer("Hi", reply_markup=markup)
# bot = Bot("7039079899:AAGxogR1d0fEmZoD0pwjIL8p9QhgoubN3tM")
# dp = Dispatcher()
    
# async def main():
#     await dp.start_polling(bot)

# if __name__ == "__main__":
#     asyncio.run(main())
