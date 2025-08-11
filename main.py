from aiogram import Bot, Dispatcher, F
from aiogram.filters.command import Command
from aiogram.types import Message
from aiogram.exceptions import TelegramAPIError
import logging
import os
import asyncio

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Отримання змінних середовища
TOKEN = os.getenv("BOT_TOKEN")
FORWARD_CHAT_ID = os.getenv("FORWARD_CHAT_ID")

if not TOKEN:
    logger.error("BOT_TOKEN не задано в змінних середовища!")
    exit(1)

try:
    FORWARD_CHAT_ID = int(FORWARD_CHAT_ID)
except (ValueError, TypeError):
    logger.error("FORWARD_CHAT_ID повинен бути числом!")
    exit(1)

# Ініціалізація бота та диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(F.photo)
async def handle_photo(message: Message):
    """Обробник фотографій."""
    try:
        await message.reply("Дякую, я отримав твій скріншот! 📸")
        logger.info(f"Отримано фото від {message.from_user.id} (@{message.from_user.username})")

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
        await message.reply("Вибачте, сталася технічна помилка. Спробуйте пізніше.")

@dp.message(F.document)
async def handle_document(message: Message):
    """Обробник документів."""
    try:
        if message.document.mime_type and message.document.mime_type.startswith("image/"):
            await message.reply("Дякую, я отримав твій скріншот! 📸")
            logger.info(f"Отримано зображення-документ від {message.from_user.id} (@{message.from_user.username})")

            await bot.forward_message(
                chat_id=FORWARD_CHAT_ID,
                from_chat_id=message.chat.id,
                message_id=message.message_id
            )
            logger.info(f"Зображення-документ переслано у чат {FORWARD_CHAT_ID}")
        else:
            await message.reply("Надішли мені скріншот (зображення) 🖼")

    except TelegramAPIError as e:
        logger.error(f"Помилка Telegram API при обробці документа: {e}")
        await message.reply("Вибачте, сталася помилка при обробці вашого файлу. Спробуйте ще раз.")
    except Exception as e:
        logger.error(f"Неочікувана помилка при обробці документа: {e}")
        await message.reply("Вибачте, сталася технічна помилка. Спробуйте пізніше.")

@dp.message(Command("start"))
@dp.message(Command("help"))
async def handle_start_help(message: Message):
    """Обробник /start та /help."""
    welcome_text = (
        "Привіт! 👋\n"
        "Я бот для отримання скріншотів.\n"
        "Надішли мені зображення або скріншот, і я його пересилатиму у потрібний чат! 📸\n\n"
        "Команди:\n"
        "/start - Почати роботу\n"
        "/help - Показати цю допомогу"
    )
    await message.reply(welcome_text)

@dp.message()
async def handle_other(message: Message):
    """Обробник інших повідомлень."""
    await message.reply("Надішли мені скріншот (зображення) 🖼")

async def on_startup(bot: Bot):
    """Запуск бота."""
    logger.info("Видаляю старий вебхук (щоб уникнути конфлікту з polling)...")
    await bot.delete_webhook(drop_pending_updates=True)
    bot_info = await bot.get_me()
    logger.info(f"Бот @{bot_info.username} запущено і готовий до роботи!")

async def on_shutdown(bot: Bot):
    """Зупинка бота."""
    logger.info("Бот зупиняється...")
    await bot.session.close()

async def main():
    await on_startup(bot)
    try:
        await dp.start_polling(bot)
    finally:
        await on_shutdown(bot)

if __name__ == "__main__":
    asyncio.run(main())
