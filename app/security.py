from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import models

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Секрретынй ключ для jwt
SECRET_KEY = "secretkey"  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# хэширования пароля
def hash_password(password: str):
    return pwd_context.hash(password)

# проверка пароля
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# созданиеву jwt токена
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# проверка токена
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
