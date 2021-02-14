from typing import List

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from app import services
from app.auth.access import authenticate_user, get_current_user
from app.auth.core import create_access_token
from app.database import engine, get_db
from app.models import Base, InventoryItem
from app.schemas import InventoryItemSchema, InventoryItemCreateSchema, InventoryItemUpdateSchema
from config import ACCESS_TOKEN_LIFETIME

app = FastAPI()


@app.on_event('startup')
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.post('/auth/token')
async def get_access_token(form_data=Depends(OAuth2PasswordRequestForm), db=Depends(get_db)):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
        )

    access_token = create_access_token(user, lifetime=ACCESS_TOKEN_LIFETIME)
    return {'access_token': access_token}


@app.get('/items', response_model=List[InventoryItemSchema])
async def list_items(
        search: str = '',
        below_threshold: bool = False,
        db=Depends(get_db),
        user=Depends(get_current_user),
):
    return await services.get_items(db, user, search, below_threshold)


@app.post('/items', response_model=InventoryItemSchema)
async def add_item(
        item: InventoryItemCreateSchema,
        db=Depends(get_db),
        user=Depends(get_current_user),
):
    return await services.create_item(db, user, **item.dict())


@app.patch('/items/{item_id}', response_model=InventoryItemSchema)
async def edit_item(
        item_id: int,
        item: InventoryItemUpdateSchema,
        db: Session = Depends(get_db),
        user=Depends(get_current_user),
):
    db_item = await services.get_item(db, user, item_id)
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid item_id specified',
        )

    return await services.update_item(db, db_item, **item.dict(exclude_unset=True))


@app.post('/items/{item_id}/change_quantity', response_model=InventoryItemSchema)
async def change_item_quantity(
        item_id: int,
        quantity_change: int,
        db: Session = Depends(get_db),
        user=Depends(get_current_user),
):
    db_item = await services.get_item(db, user, item_id)
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid item_id specified',
        )

    if db_item.quantity + quantity_change < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Quantity cannot become negative',
        )

    await services.update_item(db, db_item, quantity=InventoryItem.quantity + quantity_change)
    # Fetch again to get updated quantity from db
    return await services.get_item(db, user, item_id)
