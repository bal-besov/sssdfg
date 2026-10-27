from pydantic import BaseModel


class GameBase(BaseModel):
    """Базовая модель игры"""
    name: str
    app_id: int
    price: float = 0.0


class GameCreate(GameBase):
    """Модель для создания игры"""
    pass


class GameResponse(GameBase):
    """Модель для ответа API"""
    id: int

    class Config:
        from_attributes = True  # Работает с SQLAlchemy моделями
