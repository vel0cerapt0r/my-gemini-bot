import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from google import genai

# 1. Получаем ключи из переменных окружения сервера
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Инициализация
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()
ai_client = genai.Client(api_key=GEMINI_API_KEY)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я твой личный ИИ-ассистент на базе Gemini. Напиши мне что-нибудь!")

@dp.message()
async def handle_message(message: types.Message):
    try:
        # Отправляем запрос к модели
        response = ai_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=message.text,
        )
        await message.answer(response.text)
    except Exception as e:
        await message.answer(f"Произошла ошибка при запросе к Gemini: {e}")

async def main():
    print("Бот успешно запущен и готов к работе!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
