from fastapi import FastAPI

from . import models
from .database import engine, Session


app = FastAPI()


@app.on_event('startup')
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(
            models.Base.metadata.create_all
        )


async def get_db():
    db = Session()
    try:
        yield db
    finally:
        await db.close()
