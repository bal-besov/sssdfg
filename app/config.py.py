from pydantic_settings import BaseSettings


class Settings(BaseSettings): #Подключение к базе данных же ^^
    API_TITLE: str = "Steam Price Analyzer"
    DEBUG: bool = True
    CORS_ORIGINS: list = ["*"]
    DATABASE_URL: str = "sqlite:///./steam.db"

    class Config:
        env_file = ".env"


settings = Settings()