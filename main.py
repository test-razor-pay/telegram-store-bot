import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import user, admin

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

dp.include_router(user.router)
dp.include_router(admin.router)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
