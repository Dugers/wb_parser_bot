from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from .main import main_handler

welcome_router = Router()

@welcome_router.message(Command(commands="start"))
async def welcome_handler(message: Message):
    await message.answer("Добро пожаловать")
    return await main_handler(message)