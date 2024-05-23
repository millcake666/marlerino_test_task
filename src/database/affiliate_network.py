from sqlalchemy.orm import relationship

from database import Base
from sqlalchemy import Column, Text, BigInteger, DateTime, func, UniqueConstraint, ForeignKey


class AffiliateNetwork(Base):
    __tablename__ = 'AffiliateNetwork'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    keitaro_id = Column(BigInteger, unique=True, nullable=True)
    name = Column(Text, nullable=False, unique=True)
    postback_url = Column(Text, nullable=True)
    offer_param = Column(Text, nullable=True)
    state = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.current_timestamp())
