from fastapi import FastAPI

from app.api.routes import router
from app.database.connection import engine
from app.database.base import Base

# IMPORTANTE: carrega todos os models
import app.models

app = FastAPI(
    title="Asset Inventory System"
)


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(router)