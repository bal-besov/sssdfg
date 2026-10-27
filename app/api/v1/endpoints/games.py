from fastapi import APIRouter, HTTPException
from typing import List

# Создаём router для этого набора маршрутов
router = APIRouter()

# Временная "база данных" (позже будет реальная БД)
GAMES_DB = [
    {"id": 1, "name": "Dota 2", "app_id": 570, "price": 0.0},
    {"id": 2, "name": "Counter-Strike 2", "app_id": 730, "price": 0.0},
    {"id": 3, "name": "PUBG", "app_id": 578080, "price": 29.99},
]


@router.get("/")
def list_games() -> List[dict]:
    """
    Получить список всех игр.

    Returns:
        List[dict]: Список игр с id, name, app_id, price

    Example:
        GET /api/v1/games
        Response: [{"id": 1, "name": "Dota 2", ...}, ...]
    """
    return GAMES_DB


@router.get("/{game_id}")
def get_game(game_id: int) -> dict:
    """
    Получить информацию об игре по ID.

    Args:
        game_id (int): ID игры в базе

    Returns:
        dict: Информация об игре

    Raises:
        HTTPException: Если игра не найдена

    Example:
        GET /api/v1/games/1
        Response: {"id": 1, "name": "Dota 2", "app_id": 570, "price": 0.0}
    """
    for game in GAMES_DB:
        if game["id"] == game_id:
            return game

    raise HTTPException(
        status_code=404,
        detail=f"Игра с ID {game_id} не найдена"
    )


@router.post("/")
def create_game(name: str, app_id: int, price: float = 0.0) -> dict:
    """
    Создать новую игру.

    Args:
        name (str): Название игры
        app_id (int): App ID в Steam
        price (float): Цена (по умолчанию 0.0)

    Returns:
        dict: Созданная игра

    Example:
        POST /api/v1/games?name=Elden%20Ring&app_id=570940&price=59.99
        Response: {"id": 4, "name": "Elden Ring", "app_id": 570940, "price": 59.99}
    """
    new_id = max(game["id"] for game in GAMES_DB) + 1
    new_game = {
        "id": new_id,
        "name": name,
        "app_id": app_id,
        "price": price
    }
    GAMES_DB.append(new_game)
    return new_game