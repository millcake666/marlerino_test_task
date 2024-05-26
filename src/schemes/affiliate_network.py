from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List
from .offer import OfferOut
from enum import Enum


class AffiliateNetworkState(Enum):
    active = 'active'
    deleted = 'deleted'


class AffiliateNetworkIn(BaseModel):
    name: str
    postback_url: Optional[str] = None
    offer_param: Optional[str] = None
    notes: Optional[str] = None

    class Config:
        from_attributes = True


class AffiliateNetworkOut(BaseModel):
    id: int
    keitaro_id: Optional[int] = None

    name: str
    postback_url: Optional[str] = None
    offer_param: Optional[str] = None
    state: Optional[AffiliateNetworkState] = None
    notes: Optional[str] = None

    created_at: datetime
    updated_at: datetime

    offers: Optional[List[OfferOut]] = None

    class Config:
        from_attributes = True


class AffiliateNetworkOutFull(BaseModel):
    id: int

    keitaro_id: Optional[int] = None
    name: str
    postback_url: Optional[str] = None
    offer_param: Optional[str] = None
    state: Optional[AffiliateNetworkState] = None
    template_name: Optional[str] = None
    pull_api_options: Optional[str] = None
    notes: Optional[str] = None

    created_at: datetime
    updated_at: datetime

    offers: Optional[List[OfferOut]] = None

    class Config:
        from_attributes = True
