from fastapi import HTTPException

from service import DefaultService
from config import get_settings
from schemes import UserIn, UserOut
from database import User


settings = get_settings()


class UserService(DefaultService):
    def create(self, user: UserIn) -> UserOut:
        try:
            model = User(**user.model_dump())
            self.session.add(model)
            self.session.commit()
            self.session.refresh(model)

            return UserOut(**model.__dict__)

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f'Internal server error while creating in db table User. Detail - {e}'
            )

    def get(self, user_id: int) -> UserOut:
        try:
            user = self.session.query(User).filter_by(id=user_id).one_or_none()

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f'Internal server error while getting from db table User. Detail - {e}'
            )

        if user is None:
            raise HTTPException(
                status_code=404,
                detail=f'User not found. The user with ID {user_id} does not exist.'
            )

        return UserOut.model_validate(user)

    def delete(self, user_id: int):
        user = self.session.get(User, user_id)

        if user:
            try:
                self.session.delete(user)
                self.session.commit()

            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f'Internal server error while deleting from db table User. Detail - {e}'
                )

        else:
            raise HTTPException(
                status_code=404,
                detail=f'User not found. The user with ID {user_id} does not exist.'
            )

    def update(self, user_id: int, user: UserIn):
        try:
            user_in_db = self.session.query(User).filter_by(id=user_id).one_or_none()

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f'Internal server error while updating in db table User. Detail - {e}'
            )

        if user_in_db is None:
            raise HTTPException(
                status_code=404,
                detail=f'User not found. The user with ID {user_id} does not exist.'
            )

        try:
            user_in_db.first_name = user.first_name
            user_in_db.last_name = user.last_name

            self.session.commit()

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f'Internal server error while updating in db table User. Detail - {e}'
            )
