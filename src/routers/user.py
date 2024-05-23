from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_session
from schemes import UserIn, UserOut
from service import UserService

router = APIRouter(
    prefix='/user',
    tags=['User']
)


@router.post('')
async def create_user(user: UserIn, db: Session = Depends(get_session)) -> UserOut:
    return UserService(db).create(user)


@router.get('/{user_id}')
async def get_user(user_id: int, db: Session = Depends(get_session)) -> UserOut:
    return UserService(db).get(user_id)


@router.delete('/{user_id}')
async def delete_user(user_id: int, db: Session = Depends(get_session)):
    return UserService(db).delete(user_id)


@router.patch('/{user_id}')
async def update_user(user_id: int, user: UserIn, db: Session = Depends(get_session)):
    return UserService(db).update(user_id, user)
