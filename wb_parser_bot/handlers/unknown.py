from aiogram import Router
from aiogram.types import Message, CallbackQuery

from .main import main_handler

unknown_router = Router()

@unknown_router.message()
@unknown_router.callback_query()
async def unknown_handler(message_or_callback: Message | CallbackQuery):
    message = message_or_callback
    if (isinstance(message_or_callback, CallbackQuery)):
        message = message_or_callback.message
    
    await message.answer("К сожалению, я вас не понял")
    return await main_handler(message_or_callback)