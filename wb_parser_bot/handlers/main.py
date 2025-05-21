from aiogram import F, Router
from aiogram.types import Message, CallbackQuery

from wb_parser_bot.keyboards import main_keyboard, CallbackDatas

main_router = Router()

@main_router.message(F.text.lower() == "главное меню")
@main_router.callback_query(F.data == CallbackDatas.MAIN_MENU.value)
async def main_handler(message_or_callback: Message | CallbackQuery):
    message = message_or_callback
    if (isinstance(message_or_callback, CallbackQuery)):
        message = message_or_callback.message
    
    await message.answer("Главное меню", reply_markup=main_keyboard)