from typing import Annotated

from passlib.context import CryptContext
from pydantic import BaseModel, Field
from sqlalchemy.orm import  Session
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from ..models import Users
from ..database import SessionLocal
from .auth import get_current_user

router = APIRouter(
    prefix='/user',
    tags=['user']
)


def get_db():
    db = SessionLocal()  # Create a new database session
    try:
        yield db  # Provide it to the request handler
    finally:
        db.close()  # Ensure the session is closed after the request

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated = 'auto')


class PasswordRequest(BaseModel):
    old_password: str
    new_password: str = Field(min_length=6)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(user:user_dependency, db:db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Users).filter(Users.id == user.get('id')).first()


@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db:db_dependency, password_request: PasswordRequest):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    if user_model is None:
        raise HTTPException(status_code=404, detail="User not found")

    if not bcrypt_context.verify(password_request.old_password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail='Wrong password provided')

    user_model.hashed_password = bcrypt_context.hash(password_request.new_password)
    db.add(user_model)
    db.commit()

@router.put("/phonenumber/{phone_number}", status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(user:user_dependency, db:db_dependency, phone_number:str):

    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    user_model.phone_number = phone_number
    db.add(user_model)
    db.commit()


