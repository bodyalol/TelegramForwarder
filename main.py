from aiogram import Bot, Dispatcher, F
from aiogram.filters.command import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.exceptions import TelegramAPIError
import logging
import os
import asyncio

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Получение переменных окружения
TOKEN = os.getenv("BOT_TOKEN")
FORWARD_CHAT_ID = os.getenv("FORWARD_CHAT_ID")

if not TOKEN:
    logger.error("BOT_TOKEN не задан в переменных окружения!")
    exit(1)

try:
    FORWARD_CHAT_ID = int(FORWARD_CHAT_ID)
except (ValueError, TypeError):
    logger.error("FORWARD_CHAT_ID должен быть числом!")
    exit(1)

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Клавиатура для старта
start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📤 Отправить квитанцию")],
        [KeyboardButton(text="ℹ️ Статус оплаты")]
    ],
    resize_keyboard=True
)

@dp.message(F.photo)
async def handle_photo(message: Message):
    """Обработчик фотографий."""
    try:
        await message.reply("Спасибо! Я получил скриншот! Ожидайте ответа оператора. ⏳")
        logger.info(f"Получено фото от {message.from_user.id} (@{message.from_user.username})")

        await bot.forward_message(
            chat_id=FORWARD_CHAT_ID,
            from_chat_id=message.chat.id,
            message_id=message.message_id
        )
        logger.info(f"Фото успешно переслано в чат ✅ {FORWARD_CHAT_ID}")

    except TelegramAPIError as e:
        logger.error(f"Ошибка Telegram API при обработке фото: {e}")
        await message.reply("Извините, произошла ошибка при обработке вашего скриншота. Попробуйте ещё раз.")
    except Exception as e:
        logger.error(f"Неожиданная ошибка при обработке фото: {e}")
        await message.reply("Извините, произошла ошибка при обработке вашего скриншота. Попробуйте ещё раз.")

@dp.message(F.document)
async def handle_document(message: Message):
    """Обработчик документов."""
    try:
        if message.document.mime_type and message.document.mime_type.startswith("image/"):
            await message.reply("Спасибо! Я получил скриншот. Ожидайте архив с игрой. 🎮")
            logger.info(f"Получено изображение-документ от {message.from_user.id} (@{message.from_user.username})")

            await bot.forward_message(
                chat_id=FORWARD_CHAT_ID,
                from_chat_id=message.chat.id,
                message_id=message.message_id
            )
            logger.info(f"Спасибо! Я получил скриншот. Ожидайте архив с игрой. 🎮 {FORWARD_CHAT_ID}")
        else:
            await message.reply("Отправь мне скриншот (изображение) 🖼")

    except TelegramAPIError as e:
        logger.error(f"Ошибка Telegram API при обработке документа: {e}")
        await message.reply("Извините, произошла ошибка при обработке вашего файла. Попробуйте ещё раз.")
    except Exception as e:
        logger.error(f"Неожиданная ошибка при обработке документа: {e}")
        await message.reply("Извините, произошла ошибка при обработке вашего файла. Попробуйте ещё раз.")

@dp.message(Command("start"))
@dp.message(Command("help"))
async def handle_start_help(message: Message):
    """Обработчик /start и /help."""
    welcome_text = (
        "Привет! 👋\n"
        "Я твой помощник для получения игр после оплаты. 🎮\n"
        "Всё просто: отправьте фото квитанции, и я проверю оплату.\n"
        "После подтверждения оператором вы сразу получите свою игру! 🚀\n\n"
        "Команды:\n"
        "/start - Начать\n"
        "/help - Помощь и инструкция"
    )
    await message.reply(welcome_text, reply_markup=start_keyboard)

@dp.message(F.text == "📤 Отправить квитанцию")
async def request_receipt(message: Message):
    """Реакция на кнопку 'Отправить квитанцию'."""
    await message.reply("Пришлите фото или скриншот вашей квитанции 🖼")

@dp.message(F.text == "ℹ️ Статус оплаты")
async def payment_status(message: Message):
    """Реакция на кнопку 'Статус оплаты'."""
    # Тут можно подключить реальную проверку платежей
    await message.reply("Ваш платёж находится в обработке ⏳\nМы уведомим вас, как только он будет подтверждён ✅")

@dp.message()
async def handle_other(message: Message):
    """Обработчик других сообщений."""
    await message.reply("Пришлите мне фото квитанции 🖼")

async def on_startup(bot: Bot):
    """Запуск бота."""
    logger.info("Удаляю старый вебхук (чтобы избежать конфликта с polling)...")
    await bot.delete_webhook(drop_pending_updates=True)
    bot_info = await bot.get_me()
    logger.info(f"Бот @{bot_info.username} запущен и готов к работе!")

async def on_shutdown(bot: Bot):
    """Остановка бота."""
    logger.info("Бот останавливается...")
    await bot.session.close()

async def main():
    await on_startup(bot)
    try:
        await dp.start_polling(bot)
    finally:
        await on_shutdown(bot)

if __name__ == "__main__":
    asyncio.run(main())
