from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_session
from service import OfferService


router = APIRouter(
    prefix='/offer',
    tags=['Offer']
)


@router.post('')
async def create_offer(db: Session = Depends(get_session)):
    return OfferService(db).create()


@router.post('/keitaro')
async def create_offer_keitaro(db: Session = Depends(get_session)):
    return OfferService(db).keitaro_create()


@router.get('')
async def get_offer(db: Session = Depends(get_session)):
    return OfferService(db).get()


@router.get('/keitaro')
async def get_offer_keitaro(db: Session = Depends(get_session)):
    return OfferService(db).keitaro_get()
