from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy import Column, Text, BigInteger, DateTime, func, ForeignKey, JSON, Boolean, ARRAY, LargeBinary


class Offer(Base):
    __tablename__ = 'Offer'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    keitaro_id = Column(BigInteger, unique=True, nullable=True)

    name = Column(Text, unique=True, nullable=True)
    group_id = Column(BigInteger, nullable=True)
    action_type = Column(Text, nullable=True)
    action_payload = Column(Text, nullable=True)
    action_options = Column(JSON, nullable=True)
    affiliate_network_id = Column(BigInteger, ForeignKey('AffiliateNetwork.id'), nullable=True)
    payout_value = Column(BigInteger, nullable=True)
    payout_currency = Column(Text, nullable=True)
    payout_type = Column(Text, nullable=True)
    state = Column(Text, nullable=True)
    payout_auto = Column(Boolean, nullable=True)
    payout_upsell = Column(Boolean, nullable=True)
    country = Column(ARRAY(Text), nullable=True)
    offer_type = Column(Text, nullable=True)
    conversion_cap_enabled = Column(Boolean, nullable=True)
    daily_cap = Column(BigInteger, nullable=True)
    notes = Column(Text, nullable=True)
    conversion_timezone = Column(Text, nullable=True)
    affiliate_network = Column(Text, nullable=True)
    alternative_offer_id = Column(BigInteger, nullable=True)
    group = Column(Text, nullable=True)
    local_path = Column(Text, nullable=True)
    preview_path = Column(Text, nullable=True)
    archive = Column(LargeBinary, nullable=True)
    archive_name = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.current_timestamp())
