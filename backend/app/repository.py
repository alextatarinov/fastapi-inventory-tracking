from sqlalchemy import select

from app.auth.core import get_hashed_password
from app.models import User


async def get_user(db, email: str) -> User:
    query = select(User).where(User.email == email)
    return (await db.execute(query)).scalar()


async def create_user(db, email: str, password):
    db.add(User(email=email, hashed_password=get_hashed_password(password)))
    await db.commit()
