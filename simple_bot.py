from aiogram import Bot, Dispatcher, F
from aiogram.filters.command import Command
from aiogram.types import Message
import logging
import os
import asyncio
from keep_alive import keep_alive

# Налаштування токена - використовуємо наданий токен
TOKEN = "8422633253:AAEYmPqmyFGe4-KmB4RJMTPYSzcMltmqAOc"
FORWARD_CHAT_ID = -1001234567890  # chat_id куди пересилати фото

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(F.photo)
async def handle_photo(message: Message):
    """Обробник фотографій"""
    try:
        await message.reply("Дякую, я отримав твій скріншот! 📸")
        await bot.forward_message(FORWARD_CHAT_ID, message.chat.id, message.message_id)
        logger.info(f"Фото від {message.from_user.username} переслано")
    except Exception as e:
        logger.error(f"Помилка: {e}")
        await message.reply("Помилка при обробці фото")

@dp.message(Command("start"))
async def handle_start(message: Message):
    """Команда /start"""
    await message.reply("Привіт! Надішли мені скріншот і я його перешлю 📸")

@dp.message()
async def handle_other(message: Message):
    """Обробник всіх інших повідомлень"""
    await message.reply("Надішли мені скріншот (зображення) 🖼")

async def main():
    """Основна функція запуску"""
    try:
        # Запускаємо keep-alive для Replit
        keep_alive()
        
        logger.info("Запуск бота...")
        
        # Перевіряємо підключення до бота
        bot_info = await bot.get_me()
        logger.info(f"Бот @{bot_info.username} готовий!")
        
        # Запускаємо polling
        await dp.start_polling(bot)
        
    except Exception as e:
        logger.error(f"Помилка запуску: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())