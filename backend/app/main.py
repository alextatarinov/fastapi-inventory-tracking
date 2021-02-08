from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from app.auth.access import authenticate_user
from app.auth.core import create_access_token
from app.database import engine, get_db
from app.models import Base
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
