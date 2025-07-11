from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.utils import executor
from datetime import datetime

# === Налаштування ===
TOKEN = "8116556200:AAEGOcOjCGOV7jlKpUOHSjvthWc4bu2Zk64"
ADMIN_ID = 7709680213
CHAT_LINK = "https://t.me/+OGwp-EusOJVjODNi"

# === Бот і диспетчер ===
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# === Стан користувача ===
user_states = {}
STATE_DEFAULT = "DEFAULT"
STATE_END = "END"

# === Привітання ===
async def send_greeting(message: types.Message):
    user_states[message.from_user.id] = STATE_DEFAULT
    await message.answer(
        "🔞 Привіт! Ти потрапив у бот, що приймає заявки до приватної спільноти *Sin Sync* — місця, де зустрічаються пари, дівчата, які поділяють інтерес до свінгу, нудизму та БДСМ.\n\n"
        "🚫 Одинаки чоловіки не допускаються.\n\n"
        "Чи хотіли б ви потрапити до нашого закритого чату?\n\n"
        "Напишіть *Так* або *Ні*.",
        parse_mode="Markdown"
    )

# === Старт або новий користувач ===
@dp.message_handler(commands=["start"])
@dp.message_handler(lambda msg: user_states.get(msg.from_user.id) is None or user_states.get(msg.from_user.id) == STATE_END)
async def handle_start(message: types.Message):
    await send_greeting(message)

# === Відповідь "Ні" ===
@dp.message_handler(Text(equals="ні", ignore_case=True))
async def handle_no(message: types.Message):
    user_states[message.from_user.id] = STATE_END
    await message.answer("Добре, якщо захочете приєднатися до чату, ми будемо вас чекати. Гарного вам дня.")

# === Відповідь "Так" ===
@dp.message_handler(Text(equals="так", ignore_case=True))
async def handle_yes(message: types.Message):
    now = datetime.now().strftime("%d.%m.%Y %H:%M")
    await message.answer(
        "💡 *Умови для вступу:*\n"
        "• Пари або дівчата від 18 років\n"
        "• Чоловіки-одинаки — не приймаються\n"
        "• Запишіть відео-кружок, в якому скажіть:\n\n"
        f"– \"Мене звати Ім'я чоловіка і Ім'я дівчини\" (або тільки ім'я — якщо одна дівчина)\n"
        f"– \"Я (ми) хочу(-мо) потрапити в чат Sin Sync\"\n"
        f"– \"На даний момент час і дата: {now}\"\n"
        "– \"Чекаю(ємо) на схвалення на вступ\"\n\n"
        "📩 Після надсилання — отримаєте посилання на чат ⚠️ на нього потрібно зайти і надіслати запит на приєднання обов'язково",
        parse_mode="Markdown"
    )

# === Обробка кружка (відео-нотатки) ===
@dp.message_handler(content_types=types.ContentType.VIDEO_NOTE)
async def handle_video_note(message: types.Message):
    try:
        username = f"@{message.from_user.username}" if message.from_user.username else "Без username"
        await bot.send_video_note(ADMIN_ID, message.video_note.file_id)
        await bot.send_message(ADMIN_ID, f"🎥 Новий кружок від {username}")

        await message.answer(
            f"✅ Ваше відео надіслано адміну.\n"
            f"Переходьте за посиланням та надішліть обов'язково запит для схвалення ⬇️\n"
            f"🔗 {CHAT_LINK}\n"
            f"🕐 Чекайте на схвалення адміном."
        )
        user_states[message.from_user.id] = STATE_END
    except Exception as e:
        await message.answer("⚠️ Сталася помилка при надсиланні відео.")
        print(f"[Помилка] {e}")

# === Будь-що інше ===
@dp.message_handler()
async def handle_other(message: types.Message):
    state = user_states.get(message.from_user.id)
    if state == STATE_END or state is None:
        await send_greeting(message)
    else:
        await message.answer("Будь ласка, напишіть *Так* або *Ні*.", parse_mode="Markdown")

# === Запуск ===
if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)

# === Мінімальний веб-сервер для Replit + UptimeRobot ===
from aiohttp import web
import threading

async def handle(request):
    return web.Response(text="Sin Sync Bot is running")

def run_webserver():
    app = web.Application()
    app.router.add_get("/", handle)
    web.run_app(app, port=8080)

threading.Thread(target=run_webserver).start()
