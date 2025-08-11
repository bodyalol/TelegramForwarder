from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
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

# Переменные окружения
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

# Память статусов пользователей
user_payment_status = {}  # user_id: "no_photo", "processing", "confirmed"

# Клавиатура
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📤 Отправить квитанцию")],
        [KeyboardButton(text="ℹ️ Статус оплаты")]
    ],
    resize_keyboard=True
)

# Инициализация
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Фильтр для запрета работы в чужих чатах
async def check_chat_allowed(message: Message) -> bool:
    return message.chat.type == "private" or message.chat.id == FORWARD_CHAT_ID

@dp.message(Command("start"))
async def cmd_start(message: Message):
    if not await check_chat_allowed(message):
        return
    user_payment_status[message.from_user.id] = "no_photo"
    await message.reply(
        "Привет! 👋\n"
        "Я помогу тебе получить игру после оплаты. 🎮\n"
        "Отправь фото квитанции через кнопку ниже.",
        reply_markup=main_keyboard
    )

@dp.message(F.text == "📤 Отправить квитанцию")
async def ask_for_photo(message: Message):
    if not await check_chat_allowed(message):
        return
    await message.reply("Отправьте фото или скриншот квитанции 📸")

@dp.message(F.photo)
async def handle_photo(message: Message):
    if not await check_chat_allowed(message):
        return
    user_payment_status[message.from_user.id] = "processing"
    await message.reply("Спасибо! Я получил скриншот! Ожидайте ответа оператора. ⏳")
    logger.info(f"Получено фото от {message.from_user.id} (@{message.from_user.username})")
    try:
        await bot.forward_message(
            chat_id=FORWARD_CHAT_ID,
            from_chat_id=message.chat.id,
            message_id=message.message_id
        )
    except TelegramAPIError as e:
        logger.error(f"Ошибка Telegram API при обработке фото: {e}")
        await message.reply("Извините, произошла ошибка при обработке вашего скриншота. Попробуйте ещё раз.")

@dp.message(F.text == "ℹ️ Статус оплаты")
async def check_status(message: Message):
    if not await check_chat_allowed(message):
        return
    status = user_payment_status.get(message.from_user.id, "no_photo")
    if status == "no_photo":
        await message.reply("Вы ещё не отправили квитанцию 📸")
    elif status == "processing":
        await message.reply("Ваш платёж находится в обработке ⏳")
    elif status == "confirmed":
        await message.reply("✅ Ваш платёж подтверждён! Ожидайте ссылку на игру.")
    else:
        await message.reply("Неизвестный статус. Отправьте квитанцию ещё раз.")

@dp.message()
async def handle_other(message: Message):
    if not await check_chat_allowed(message):
        return
    await message.reply("Пожалуйста, используйте кнопки ниже ⬇️", reply_markup=main_keyboard)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
