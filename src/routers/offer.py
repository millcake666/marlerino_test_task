from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse

from database import get_session
from schemes import OfferIn, OfferOut
from service import OfferService

router = APIRouter(
    prefix='/offer',
    tags=['Offer']
)


@router.post('')
async def create_offer(offer: OfferIn, db: Session = Depends(get_session)):
    return OfferService(db).create(offer)


@router.post('/archive/{offer_id}')
async def upload_archive(offer_id: int, archive: UploadFile = File(), db: Session = Depends(get_session)):
    return await OfferService(db).upload_archive(offer_id, archive)


@router.get('/archive/{offer_id}')
async def download_archive(offer_id: int, db: Session = Depends(get_session)) -> StreamingResponse:
    return await OfferService(db).download_archive(offer_id)


@router.post('/keitaro/{offer_id}')
async def create_offer_keitaro(offer_id: int, db: Session = Depends(get_session)) -> OfferOut:
    return OfferService(db).keitaro_create(offer_id)


@router.get('/{offer_id}')
async def get_offer(offer_id: int, db: Session = Depends(get_session)) -> OfferOut:
    return OfferService(db).get(offer_id)


@router.get('/keitaro/{offer_id}')
async def get_offer_keitaro(offer_id: int, db: Session = Depends(get_session)):
    return OfferService(db).keitaro_get(offer_id)
