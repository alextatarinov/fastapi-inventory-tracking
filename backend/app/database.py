from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from config import DATABASE_URL

engine = create_async_engine(str(DATABASE_URL), echo=True, future=True)
Session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()


async def get_db() -> Session:
    db = Session()
    try:
        yield db
    finally:
        await db.close()
