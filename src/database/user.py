from sqlalchemy.orm import relationship

from database import Base
from sqlalchemy import Column, Text, BigInteger, DateTime, func, UniqueConstraint, ForeignKey


class User(Base):
    __tablename__ = 'User'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    first_name = Column(Text, nullable=False)
    last_name = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
