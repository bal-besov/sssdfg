from fastapi import APIRouter
from app.api.v1.endpoints import games, prices, analytics

router = APIRouter()

router.include_router(games.router, prefix="/games", tags=["games"])
router.include_router(prices.router, prefix="/prices", tags=["prices"])
router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])