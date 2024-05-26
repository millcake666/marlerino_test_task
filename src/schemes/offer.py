from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List, Dict
from enum import Enum


class OfferType(Enum):
    local = 'local'
    external = 'external'
    preloaded = 'preloaded'
    action = 'action'


class OfferPayoutType(Enum):
    cpa = 'CPA'
    cpc = 'CPC'


class OfferState(Enum):
    active = 'active'
    deleted = 'deleted'


class OfferIn(BaseModel):
    name: str
    group_id: Optional[int] = None
    offer_type: Optional[OfferType] = None
    action_type: Optional[str] = None
    action_payload: Optional[str | object] = None
    affiliate_network_id: Optional[int] = None
    payout_value: Optional[int] = None
    payout_currency: Optional[str] = None
    payout_type: Optional[OfferPayoutType] = None
    state: Optional[OfferState] = None
    payout_auto: Optional[bool] = None
    payout_upsell: Optional[bool] = None
    country: Optional[List[str]] = None
    notes: Optional[str] = None
    conversion_cap_enabled: Optional[bool] = None
    daily_cap: Optional[int] = None
    conversion_timezone: Optional[str] = None
    alternative_offer_id: Optional[int] = None

    class Config:
        from_attributes = True
        use_enum_values = True


class OfferOut(BaseModel):
    id: int
    keitaro_id: Optional[int] = None

    name: str
    group_id: Optional[int] = None
    action_type: Optional[str] = None
    action_payload: Optional[str | object] = None
    action_options: Optional[Dict] = None
    affiliate_network_id: Optional[int] = None
    payout_value: Optional[int] = None
    payout_currency: Optional[str] = None
    payout_type: Optional[OfferPayoutType] = None
    state: Optional[OfferState] = None
    payout_auto: Optional[bool] = None
    payout_upsell: Optional[bool] = None
    country: Optional[List[str]] = None
    offer_type: Optional[OfferType] = None
    conversion_cap_enabled: Optional[bool] = None
    daily_cap: Optional[int] = None
    notes: Optional[str] = None
    conversion_timezone: Optional[str] = None
    affiliate_network: Optional[str] = None
    alternative_offer_id: Optional[int] = None
    group: Optional[str] = None
    local_path: Optional[str] = None
    preview_path: Optional[str] = None
    archive_name: Optional[str] = None

    values: Optional[List[Dict]] = None

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        use_enum_values = True
