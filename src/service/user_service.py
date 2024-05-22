from fastapi import HTTPException

from service import DefaultService
from config import get_settings
from sqlalchemy.dialects.postgresql import insert
from scheme import UserIn, UserOut
from database import User


settings = get_settings()


class UserService(DefaultService):
    def create(self, user: UserIn) -> int:
        q = insert(User).values(user.model_dump())
        s = q.on_conflict_do_nothing().returning(User.id)

        user_id = self.session.execute(s).scalar()
        self.session.commit()

        return user_id

    def get(self, user_id: int) -> UserOut:
        user = self.session.query(User).filter_by(id=user_id).one_or_none()
        if user is None:
            raise HTTPException(
                status_code=404,
                detail=f'User not found. The user with ID {user_id} does not exist.'
            )

        return UserOut.model_validate(user)
