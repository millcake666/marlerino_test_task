from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_session
from service import AffiliateNetworkService
from schemes import AffiliateNetworkIn, AffiliateNetworkOut, AffiliateNetworkOutFull

router = APIRouter(
    prefix='/affiliate_network',
    tags=['AffiliateNetwork']
)


@router.post('/{user_id}')
async def create_affiliate_network(user_id: int,
                                   affiliate_network: AffiliateNetworkIn,
                                   db: Session = Depends(get_session)) -> AffiliateNetworkOut:
    return AffiliateNetworkService(db).create(user_id, affiliate_network)


@router.post('/keitaro/{user_id}/{affiliate_network_id}')
async def create_affiliate_network_keitaro(user_id: int,
                                           affiliate_network_id: int,
                                           db: Session = Depends(get_session)) -> AffiliateNetworkOut:
    return AffiliateNetworkService(db).keitaro_create(user_id, affiliate_network_id)


@router.get('/{affiliate_network_id}')
async def get_affiliate_network(affiliate_network_id: int,
                                db: Session = Depends(get_session)) -> AffiliateNetworkOut:
    return AffiliateNetworkService(db).get(affiliate_network_id)


@router.get('/keitaro/{affiliate_network_id}')
async def get_affiliate_network_keitaro(affiliate_network_id: int,
                                        db: Session = Depends(get_session)) -> AffiliateNetworkOutFull:
    return AffiliateNetworkService(db).keitaro_get(affiliate_network_id)
