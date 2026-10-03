from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="My API")


class UserCreate(BaseModel):
    name: str
    email: str


@app.get("/")
async def root():
    return {
        "message": "API is running"
    }
