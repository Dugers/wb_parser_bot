from aiogram import Router

from .main import main_router
from .position import position_router

product_analys_router = Router()

children_routers = [
    main_router,
    position_router
]

product_analys_router.include_routers(*children_routers)