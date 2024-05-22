import abc
from sqlalchemy.orm import Session


class DefaultService(abc.ABC):
    def __init__(self, session):
        self.__session = session

    @property
    def session(self) -> Session:
        return self.__session
