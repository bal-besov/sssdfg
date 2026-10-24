import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from app.main import create_app

app = FastAPI(title="My API")

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True    )

class UserCreate(BaseModel):
    name: str
    email: str


@app.get("/")
async def root():
    return {
        "message": "API is running"
    }
