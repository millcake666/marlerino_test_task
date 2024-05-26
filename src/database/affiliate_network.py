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

    offers = relationship('Offer', secondary='AffiliateNetworkToOffer')


class AffiliateNetworkToOffer(Base):
    __tablename__ = 'AffiliateNetworkToOffer'

    affiliate_network_id = Column(BigInteger, ForeignKey('AffiliateNetwork.id'), primary_key=True)
    offer_id = Column(BigInteger, ForeignKey('Offer.id'), primary_key=True)

    __table_args__ = (
        UniqueConstraint('affiliate_network_id', 'offer_id', name='_affiliate_network_offer_uc'),
    )
