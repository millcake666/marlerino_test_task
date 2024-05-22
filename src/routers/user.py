from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_session
from scheme import UserIn, UserOut
from service import UserService


router = APIRouter(
    prefix='/user',
    tags=['User']
)


@router.post('')
async def create_user(user: UserIn, db: Session = Depends(get_session)) -> int:
    return UserService(db).create(user)


@router.get('/{user_id}')
async def get_user(user_id: int, db: Session = Depends(get_session)):
    return UserService(db).get(user_id)
