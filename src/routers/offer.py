from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_session
from service import OfferService


router = APIRouter(
    prefix='/offer',
    tags=['Offer']
)


@router.post('')
async def add_offer(db: Session = Depends(get_session)):
    return OfferService(db).create()


@router.post('/keitaro')
async def add_offer(db: Session = Depends(get_session)):
    return OfferService(db).keitaro_add()


@router.get('')
async def get_offer(db: Session = Depends(get_session)):
    return OfferService(db).get()
