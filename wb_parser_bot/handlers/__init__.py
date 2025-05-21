from aiogram import Router

from .welcome import welcome_router
from .cancel import cancel_router
from .main import main_router
from .product_analys import product_analys_router
from .unknown import unknown_router

handlers_router = Router()

children_routers = [
    welcome_router,
    cancel_router,
    main_router,
    product_analys_router,
    unknown_router
]

handlers_router.include_routers(*children_routers)