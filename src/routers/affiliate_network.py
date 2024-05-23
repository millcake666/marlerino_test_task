from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_session
from service import AffiliateNetworkService
from schemes import AffiliateNetworkIn, AffiliateNetworkOut


router = APIRouter(
    prefix='/affiliate_network',
    tags=['AffiliateNetwork']
)


@router.post('')
async def create_affiliate_network(affiliate_network: AffiliateNetworkIn, db: Session = Depends(get_session)) -> (
        AffiliateNetworkOut):
    return AffiliateNetworkService(db).create(affiliate_network)


@router.post('/keitaro')
async def create_affiliate_network_keitaro(db: Session = Depends(get_session)) -> int:
    return AffiliateNetworkService(db).keitaro_create()


@router.get('')
async def get_affiliate_network(db: Session = Depends(get_session)):
    return AffiliateNetworkService(db).get()


@router.get('/keitaro')
async def get_affiliate_network_keitaro(db: Session = Depends(get_session)):
    return AffiliateNetworkService(db).keitaro_get()
