from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from enum import Enum


class AffiliateNetworkState(Enum):
    active = 'active'
    deleted = 'deleted'


class AffiliateNetworkIn(BaseModel):
    name: str
    postback_url: Optional[str] = None
    offer_param: Optional[str] = None
    notes: Optional[str] = None


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
