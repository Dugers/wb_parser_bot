from aiogram.fsm.state import State, StatesGroup

class ProductAnalysState(StatesGroup):
    product_id = State()
    process = State()