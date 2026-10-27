from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import router as v1_router
from app.config import settings


def create_app() -> FastAPI:
    """Инициализирует и настраивает FastAPI приложение"""

    app = FastAPI(
        title="Steam Price Analyzer",
        description="API для анализа цен на игры Steam",
        version="1.0.0"
        debug = settings.DEBUG
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(v1_router)

    # test route
    @app.get("/")
    def read_root():
        """Главная страница"""
        return {
            "message": "Welcome to Steam Price Analyzer",
            "docs": "/docs",
            "docs_redoc": "/redoc"
        }

    # Маршруты
    app.include_router(v1_router, prefix="/api/v1")

    def health_check():
        """Проверка что сервер работает"""

    return {"status": "ok"}

    return app
# для uvicorn
app = create_app()