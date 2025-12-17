from typing import Annotated
from fastapi import Depends, HTTPException
from authx.exceptions import JWTDecodeError

from sqlalchemy.ext.asyncio import AsyncSession
from database.session import get_session
from core.security import security


AsyncSessionDep = Annotated[AsyncSession, Depends(get_session)]
SecurityDep = Depends(security.access_token_required)
