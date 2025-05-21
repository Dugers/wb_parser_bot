import re
import asyncio
import inspect
from typing import Awaitable, Callable, Dict, List, Optional
from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from wb_parser_bot.keyboards import CallbackDatas, cancel_keyboard
from wb_parser_bot.services import ParserService, ProductGet, ProductFind, KeywordsGenerator
from wb_parser_bot.states import ProductAnalysState

position_router = Router()

@position_router.callback_query(F.data == CallbackDatas.PRODUCT_ANALYS_PLACE_IN_SEARCH_BY_KEYWORDS.value)
async def position_start_handler(callback: CallbackQuery | Message, state: FSMContext):
    message = callback
    if (isinstance(callback, CallbackQuery)):
        message = callback.message
    await state.set_state(ProductAnalysState.product_id)
    await message.answer("Введите ссылку на товар", reply_markup=cancel_keyboard)

@position_router.message(ProductAnalysState.product_id)
async def position_product_id_handler(message: Message, state: FSMContext):
    try:
        product_id = parse_product_id_from_url(message.text)
    except:
        return await message.answer("Ссылка на товар не корректна, попробуйте снова", reply_markup=cancel_keyboard)
    await state.set_state(ProductAnalysState.process)

    status_message = await message.answer(f"✅ Получен id товара: {product_id}")
    product = await do_action(action=parse_product_info(product_id), 
                    status_message=status_message,
                    state=state, 
                    success_text="Информация о товаре получена!",
                    error_text="Ошибка при получении информации о товаре.",
                    wait_text="Получаем информацию о товаре")

    query = product.imt_name + ' ' + (product.description if product.description else '')
    keywords = await do_action(action=lambda: parse_keywords(query), 
                    status_message=status_message,
                    state=state, 
                    success_text="Ключевые слова получены!",
                    error_text="Ошибка при получении ключевых слов.",
                    wait_text="Получаем ключевые слова")
    
    products_by_keyword = await do_action(action=get_products_by_queryies(keywords), 
                    status_message=status_message,
                    state=state,
                    success_text="Товары по ключевым словам получены!",
                    error_text="Ошибка при получении товаров по ключевых словам.",
                    wait_text="Получаем товары по ключевым словам")
    
    report_text = await do_action(action=lambda: make_report(product_id, products_by_keyword), 
                    status_message=status_message,
                    state=state,
                    success_text="Запрос выполнен!",
                    error_text="Ошибка при определении позиции товара.",
                    wait_text="Определяем позицию товара при запросе по ключевым словам")
    await status_message.edit_text(f"🎉 Результат анализа 🎉\n{report_text}")
    
async def do_action[T](action: Callable[[], T] | Awaitable[T], status_message: Message, state: FSMContext, success_text: str, error_text: str, wait_text: str) -> T:
    loop = asyncio.get_event_loop()
    wait_message_task = loop.create_task(do_wait_message(status_message, wait_text))
    try:
        if (inspect.isawaitable(action)):
            result = await action
        else:
            result = action()
        wait_message_task.cancel()
        await status_message.edit_text(f"✅ {success_text}")
        return result
    except:
        wait_message_task.cancel()
        return await show_error_and_redirect(status_message, state, error_text)
    
def parse_product_id_from_url(url: str):
    match = re.search(r'/catalog/(\d+)/', url)
    product_id = int(match.group(1))
    ParserService.validate_id(product_id)
    return product_id

async def parse_product_info(product_id: int) -> ProductGet:
    parser = ParserService()
    return await parser.get_product(product_id)

def parse_keywords(query: str) -> List[str]:
    keywords_generator = KeywordsGenerator()
    return keywords_generator.generate(query)

async def show_error_and_redirect(status_message: Message, state: FSMContext, text: str):
    await status_message.edit_text(f"❌ {text} Давайте попробуем снова.")
    await state.clear()
    return position_start_handler(status_message, state)

async def do_wait_message(status_message: Message, base_text: str):
    while True:
        for count_dots in range(1, 4):
            await asyncio.sleep(.5)
            await status_message.edit_text(f"⏳ {base_text}{'.'*count_dots}")

async def get_products_by_queryies(queries: List[str]) -> Dict[str, List[ProductFind]]:
    parser = ParserService()
    products_by_query = {}
    for query in queries:
        products_by_query[query] = await parser.find_products(query)
    return products_by_query

def find_product_id_in_find_products_list(product_id: int, products: List[ProductFind]) -> Optional[int]:
    for product_index in range(len(products)):
        if (product_id == products[product_index].id):
            return product_index
    
def make_report(product_id: int, products_by_keyword: Dict[str, List[ProductFind]]) -> str:
    text = ""    
    for keyword in products_by_keyword:
        product_index = find_product_id_in_find_products_list(product_id, products_by_keyword[keyword]) or ">100"
        text += f"По запросу \"{keyword}\" указанный товар имеет позицию: {product_index}\n"
    return text