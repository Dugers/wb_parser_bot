from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from enum import Enum

from wb_parser_bot.config import settings

class CallbackDatas(Enum):
    MAIN_MENU = "main"
    PRODUCT_ANALYS = "product_analys"
    PRODUCT_ANALYS_PLACE_IN_SEARCH_BY_KEYWORDS = "product_analys_place_in_search_by_keywords"

main_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Связаться с разработчиком", url=settings.bot.developer_url)],
    [InlineKeyboardButton(text="Анализ товара", callback_data=CallbackDatas.PRODUCT_ANALYS)]
])

product_analys_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Позиция товара в выдаче по ключевым запросам", callback_data=CallbackDatas.PRODUCT_ANALYS_PLACE_IN_SEARCH_BY_KEYWORDS)],
    [InlineKeyboardButton(text="Главное меню", callback_data=CallbackDatas.MAIN_MENU)]
])

cancel_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Отмена")]
], resize_keyboard=True)