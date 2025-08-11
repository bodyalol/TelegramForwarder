from aiogram import Bot, Dispatcher, F
from aiogram.filters.command import Command
from aiogram.types import Message
from aiogram.exceptions import TelegramAPIError, TelegramNetworkError
import logging
import os
import asyncio
from keep_alive import keep_alive

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Для тестування використовуємо наданий токен
TOKEN = "8422633253:AAEYmPqmyFGe4-KmB4RJMTPYSzcMltmqAOc"

# Chat ID для пересилання повідомлень - потрібно буде налаштувати
FORWARD_CHAT_ID = os.getenv("FORWARD_CHAT_ID", "-1001234567890")

try:
    FORWARD_CHAT_ID = int(FORWARD_CHAT_ID)
except ValueError:
    logger.error("FORWARD_CHAT_ID повинен бути числом!")
    exit(1)

# Ініціалізація бота та диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(F.photo)
async def handle_photo(message: Message):
    """
    Обробник фотографій. Дякує користувачу та пересилає фото у вказаний чат.
    """
    try:
        # Відповідаємо користувачу українською
        await message.reply("Дякую, я отримав твій скріншот! 📸")
        logger.info(f"Отримано фото від користувача {message.from_user.id} (@{message.from_user.username})")
        
        # Пересилаємо фото у вказаний чат
        await bot.forward_message(
            chat_id=FORWARD_CHAT_ID,
            from_chat_id=message.chat.id,
            message_id=message.message_id
        )
        logger.info(f"Фото переслано у чат {FORWARD_CHAT_ID}")
        
    except TelegramAPIError as e:
        logger.error(f"Помилка Telegram API при обробці фото: {e}")
        await message.reply("Вибачте, сталася помилка при обробці вашого скріншота. Спробуйте ще раз.")
    except Exception as e:
        logger.error(f"Неочікувана помилка при обробці фото: {e}")
        await message.reply("Вибачте, сталася технічна помилка. Спробуйте ще раз пізніше.")

@dp.message(F.document)
async def handle_document(message: Message):
    """
    Обробник документів. Перевіряє чи це зображення та обробляє відповідно.
    """
    try:
        # Перевіряємо чи документ є зображенням
        if message.document.mime_type and message.document.mime_type.startswith('image/'):
            # Обробляємо як зображення
            await message.reply("Дякую, я отримав твій скріншот! 📸")
            logger.info(f"Отримано зображення-документ від користувача {message.from_user.id} (@{message.from_user.username})")
            
            # Пересилаємо у вказаний чат
            await bot.forward_message(
                chat_id=FORWARD_CHAT_ID,
                from_chat_id=message.chat.id,
                message_id=message.message_id
            )
            logger.info(f"Зображення-документ переслано у чат {FORWARD_CHAT_ID}")
        else:
            # Це не зображення
            await message.reply("Надішли мені скріншот (зображення) 🖼")
            
    except TelegramAPIError as e:
        logger.error(f"Помилка Telegram API при обробці документа: {e}")
        await message.reply("Вибачте, сталася помилка при обробці вашого файлу. Спробуйте ще раз.")
    except Exception as e:
        logger.error(f"Неочікувана помилка при обробці документа: {e}")
        await message.reply("Вибачте, сталася технічна помилка. Спробуйте ще раз пізніше.")

@dp.message(Command("start"))
@dp.message(Command("help"))
async def handle_start_help(message: Message):
    """
    Обробник команд /start та /help
    """
    try:
        welcome_text = (
            "Привіт! 👋\n"
            "Я бот для отримання скріншотів.\n"
            "Надішли мені зображення або скріншот, і я його обробляю! 📸\n\n"
            "Команди:\n"
            "/start - Почати роботу\n"
            "/help - Показати цю допомогу"
        )
        await message.reply(welcome_text)
        logger.info(f"Відправлено привітання користувачу {message.from_user.id} (@{message.from_user.username})")
        
    except Exception as e:
        logger.error(f"Помилка при відправці привітання: {e}")

@dp.message()
async def handle_other(message: Message):
    """
    Обробник всіх інших типів повідомлень
    """
    try:
        await message.reply("Надішли мені скріншот (зображення) 🖼")
        logger.info(f"Отримано не-фото повідомлення від користувача {message.from_user.id} (@{message.from_user.username})")
        
    except Exception as e:
        logger.error(f"Помилка при відповіді на не-фото повідомлення: {e}")

async def on_startup():
    """
    Функція, що виконується при запуску бота
    """
    logger.info("Бот запущено!")
    try:
        bot_info = await bot.get_me()
        logger.info(f"Бот @{bot_info.username} готовий до роботи")
    except Exception as e:
        logger.error(f"Помилка при отриманні інформації про бота: {e}")

async def on_shutdown():
    """
    Функція, що виконується при зупинці бота
    """
    logger.info("Бот зупиняється...")
    await bot.session.close()

async def main():
    """
    Головна функція запуску бота
    """
    try:
        # Запускаємо keep-alive сервер для Replit
        keep_alive()
        
        # Запускаємо бота
        logger.info("Запуск Telegram бота...")
        await on_startup()
        await dp.start_polling(bot)
        
    except KeyboardInterrupt:
        logger.info("Бота зупинено користувачем")
    except Exception as e:
        logger.error(f"Критична помилка: {e}")
    finally:
        await on_shutdown()

if __name__ == "__main__":
    asyncio.run(main())
