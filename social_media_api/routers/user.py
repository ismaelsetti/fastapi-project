import logging

from fastapi import APIRouter, HTTPException, status

from social_media_api.database import database, user_table
from social_media_api.models.user import UserIn
from social_media_api.security import (
    authenticate_user,
    create_access_token,
    get_password_hash,
    get_user,
)

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/register", status_code=201)
async def register_user(user: UserIn):
    if await get_user(user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with that email already exists",
        )
    hashed_password = get_password_hash(user.password)
    query = user_table.insert().values(email=user.email, password=hashed_password)

    logger.debug(query)

    await database.execute(query)
    return {"detail": "User Created."}


@router.post("/token")
async def login(user: UserIn):
    user = await authenticate_user(user.email, user.password)
    access_token = create_access_token(user.email)
    return {"access_token": access_token, "token_type": "bearer"}
