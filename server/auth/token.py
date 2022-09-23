from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from prisma.models import Token
from server.database import db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/users/login")


async def get_token(token_string: str = Depends(oauth2_scheme)):
    token = await db.token.find_unique(
        where={"access_token": token_string}, include={"user": True}
    )
    now = datetime.utcnow().replace(tzinfo=None)
    expired = token.expiry_date.replace(tzinfo=None) < now
    if token:
        if not expired:
            return token
        # delete expired token
        await db.token.delete(where={"id": token.id})
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
        headers={"WWW-Authenticate": "Bearer"},
    )


async def get_user(token: Token = Depends(get_token)):
    user = token.user
    print("user", user)
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
        headers={"WWW-Authenticate": "Bearer"},
    )
