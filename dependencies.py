from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from auth import verify_token

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)

def get_current_user(
        token: str = Depends(oauth2_scheme)
):
    email = verify_token(token)

    if not email:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )
    
    return email