from typing import Annotated
from fastapi import Depends, HTTPException, Request
from authx.exceptions import JWTDecodeError

from sqlalchemy.ext.asyncio import AsyncSession
from database.session import get_session
from core.security import security


AsyncSessionDep = Annotated[AsyncSession, Depends(get_session)]


async def get_current_user(request: Request):
    try:
        token = await security._get_token_from_request(request)
        if not token or not token.token:
            raise HTTPException(status_code=401, detail="No token provided")
        return security._decode_token(token.token)
    except JWTDecodeError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    except Exception:
        raise HTTPException(status_code=401, detail="Unauthorized")


SecurityDep = Annotated[str, Depends(get_current_user)]
