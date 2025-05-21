from aiogram import F, Router
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from .main import main_handler

cancel_router = Router()

@cancel_router.message(F.text.lower() == "отмена")
async def cancel_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Действие отменено", reply_markup=ReplyKeyboardRemove())
    return await main_handler(message)