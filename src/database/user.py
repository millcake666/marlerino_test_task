from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy import Column, Text, BigInteger, DateTime, func, UniqueConstraint, ForeignKey


class User(Base):
    __tablename__ = 'User'

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    first_name = Column(Text, nullable=False)
    last_name = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.current_timestamp())

    affiliate_networks = relationship('AffiliateNetwork', secondary='UserToAffiliateNetwork')


class UserToAffiliateNetwork(Base):
    __tablename__ = 'UserToAffiliateNetwork'

    user_id = Column(BigInteger, ForeignKey('User.id'), primary_key=True)
    affiliate_network_id = Column(BigInteger, ForeignKey('AffiliateNetwork.id'), primary_key=True)

    __table_args__ = (
        UniqueConstraint('user_id', 'affiliate_network_id', name='_user_affiliate_network_uc'),
    )
