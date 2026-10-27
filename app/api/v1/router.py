from fastapi import APIRouter
from app.api.v1.endpoints import games, prices, analytics

# Создаём главный router для v1
v1_router = APIRouter(prefix="/api/v1")

# Подключаем маршруты игр
v1_router.include_router(
    games.router,
    prefix="/games",
    tags=["Games"]  # В Swagger UI будут сгруппированы под "Games"
)

# Позже добавим сюда маршруты цен и аналитики:
# v1_router.include_router(
#     prices.router,
#     prefix="/prices",
#     tags=["Prices"]
# )
#
# v1_router.include_router(
#     analytics.router,
#     prefix="/analytics",
#     tags=["Analytics"]
# )
