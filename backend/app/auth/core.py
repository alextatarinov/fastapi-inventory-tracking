from datetime import datetime, timedelta

import jwt
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from config import SECRET_KEY


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
ALGORITHM = 'HS256'

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_hashed_password(password):
    return pwd_context.hash(password)


def create_access_token(user, lifetime: timedelta = timedelta(minutes=15)):
    expire = datetime.utcnow() + lifetime
    data = {
        'sub': user.email,
        'exp': expire,
    }
    encoded_jwt = jwt.encode(data, str(SECRET_KEY), algorithm=ALGORITHM)
    return encoded_jwt
