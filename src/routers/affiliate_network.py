from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_session
from service import AffiliateNetworkService


router = APIRouter(
    prefix='/affiliate_network',
    tags=['AffiliateNetwork']
)


@router.post('')
async def add_affiliate_network(db: Session = Depends(get_session)):
    return AffiliateNetworkService(db).create()


@router.post('/keitaro')
async def add_affiliate_network(db: Session = Depends(get_session)):
    return AffiliateNetworkService(db).keitaro_add()


@router.get('')
async def get_affiliate_network(db: Session = Depends(get_session)):
    return AffiliateNetworkService(db).get()
