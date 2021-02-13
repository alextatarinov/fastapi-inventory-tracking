from typing import Optional

import jwt
from fastapi import Depends, HTTPException
from jwt import PyJWTError
from starlette import status

from app.auth.core import ALGORITHM, oauth2_scheme, verify_password
from app.database import get_db
from app.models import User
from app.services import get_user
from config import SECRET_KEY


async def authenticate_user(db, email: str, password: str) -> Optional[User]:
    user = await get_user(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


async def get_current_user(db=Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
    )
    try:
        payload = jwt.decode(token, str(SECRET_KEY), algorithms=[ALGORITHM])
        email: str = payload.get('sub')
        if email is None:
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception

    user = await get_user(db, email=email)
    if user is None:
        raise credentials_exception
    return user
