from aiogram import F, Router
from aiogram.types import CallbackQuery

from wb_parser_bot.keyboards import product_analys_keyboard, CallbackDatas

main_router = Router()

@main_router.callback_query(F.data == CallbackDatas.PRODUCT_ANALYS.value)
async def main_handler(callback: CallbackQuery):
    message = callback.message
    await message.answer("Меню анализа товаров", reply_markup=product_analys_keyboard)