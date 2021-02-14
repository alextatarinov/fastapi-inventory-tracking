from typing import List

from sqlalchemy import select, or_
from sqlalchemy.orm import Session

from app.auth.core import get_hashed_password
from app.models import InventoryItem, User


async def get_user(db: Session, email: str) -> User:
    query = select(User).where(User.email == email)
    return (await db.execute(query)).scalar_one()


async def create_user(db: Session, email: str, password) -> User:
    db_user = User(email=email, hashed_password=get_hashed_password(password))
    db.add(db_user)
    await db.commit()
    return db_user


async def get_items(db: Session, user: User, search: str = '', below_threshold: bool = False) -> List[InventoryItem]:
    query = select(InventoryItem).where(
        InventoryItem.user_id == user.id
    )
    if search:
        query = query.where(
            or_(
                InventoryItem.name.ilike(f'{search}%'),
                InventoryItem.manufacturer.ilike(f'{search}%'),
            )
        )

    if below_threshold:
        query = query.where(
            InventoryItem.quantity < InventoryItem.threshold
        )

    return list((await db.execute(query)).scalars())


async def get_item(db: Session, user: User, item_id: int) -> InventoryItem:
    query = select(InventoryItem).where(
        InventoryItem.user_id == user.id,
        InventoryItem.id == item_id,
    )
    return (await db.execute(query)).scalar()


async def create_item(db: Session, user: User, **kwargs) -> InventoryItem:
    db_item = InventoryItem(**kwargs, user_id=user.id)
    db.add(db_item)
    await db.commit()
    return db_item


async def update_item(db: Session, db_item: InventoryItem, **kwargs) -> InventoryItem:
    for field, value in kwargs.items():
        setattr(db_item, field, value)
    await db.commit()
    return db_item
