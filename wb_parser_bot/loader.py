from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from .config import settings
from .handlers import handlers_router

bot = Bot(token=settings.bot.token)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

dp.include_router(handlers_router)

async def load():
    await dp.start_polling(bot)