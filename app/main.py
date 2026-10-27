from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import router as v1_router
from app.config import settings


def create_app() -> FastAPI:
    app = FastAPI(
        title="Steam Price Analyzer",
        description="API для анализа цен на игры Steam",
        version="1.0.0"
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Маршруты
    app.include_router(v1_router, prefix="/api/v1")

    return app