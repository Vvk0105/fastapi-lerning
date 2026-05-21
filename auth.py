from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext

SECURITY_KEY = "myseckey"

ALGORITHM = "HS256"

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(
        plain_password,
        hashed_password
    )

def create_access_token(data: dict):
    to_encode = data.copy()
    
    expire = datetime.now(timezone.utc) + timedelta(hours=1)
    
    to_encode.update({"exp": expire})

    encode_jwt = jwt.encode(
        to_encode,
        SECURITY_KEY,
        algorithm=ALGORITHM
    )

    return encode_jwt
