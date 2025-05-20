from fastapi import APIRouter

from .endpoints import basket_router, mushroom_router

main_router = APIRouter()
main_router.include_router(basket_router, prefix='/baskets', tags=['Baskets'])
main_router.include_router(
    mushroom_router, prefix='/mushrooms', tags=['Mushrooms']
)
