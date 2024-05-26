from fastapi import UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse

from schemes import OfferIn, OfferOut
from service import DefaultService
from config import get_settings
from database import Offer, AffiliateNetwork, AffiliateNetworkToOffer
from base64 import b64encode, b64decode
from io import BytesIO
import requests
from service.keitaro_auth import KeitaroAuth


settings = get_settings()
keitaro_auth = KeitaroAuth()


class OfferService(DefaultService):
    def create(self, offer: OfferIn) -> OfferOut:
        r_exist_offers_in_keitaro = requests.get(
            url=f'{settings.KEITARO_DOMAIN}/{settings.KEITARO_API_DOMAIN}/offers',
            headers=keitaro_auth.headers_with_auth()
        )
        if r_exist_offers_in_keitaro.status_code == 200 and r_exist_offers_in_keitaro.json() is not None:
            exist_offers_in_keitaro = r_exist_offers_in_keitaro.json()
            for exist_offer_in_keitaro in exist_offers_in_keitaro:
                if exist_offer_in_keitaro.get('name') == offer.name:
                    raise HTTPException(status_code=400, detail='This offer name is already exist in Keitaro')

        offer_model = Offer(**offer.model_dump())
        self.session.add(offer_model)
        self.session.commit()
        self.session.refresh(offer_model)

        affiliate_network_model = self.session.query(AffiliateNetwork).filter_by(
            id=offer.affiliate_network_id
        ).one_or_none()
        affiliate_network_to_offer_model = AffiliateNetworkToOffer(
            affiliate_network_id=affiliate_network_model.id,
            offer_id=offer_model.id
        )
        self.session.add(affiliate_network_to_offer_model)
        self.session.commit()

        return OfferOut.model_validate(offer_model)

    async def upload_archive(self, offer_id: int, archive: UploadFile = File()):
        offer = self.session.query(Offer).filter_by(id=offer_id).one_or_none()
        file = await archive.read()
        offer.archive = b64encode(file)
        offer.archive_name = archive.filename
        self.session.commit()

    async def download_archive(self, offer_id: int) -> StreamingResponse:
        offer = self.session.query(Offer).filter_by(id=offer_id).one_or_none()
        bytes_archive = b64decode(offer.archive)
        return StreamingResponse(
            content=BytesIO(bytes_archive),
            headers={
                'Content-Disposition': f'attachment; filename="{offer.archive_name}"',
                'Content-Length': str(len(bytes_archive))},
            media_type="application/zip")

    def keitaro_create(self, offer_id: int) -> OfferOut:
        offer_model = self.session.query(Offer).filter_by(id=offer_id).one_or_none()
        affiliate_network_model = self.session.query(AffiliateNetwork).filter_by(id=offer_model.affiliate_network_id).one_or_none()

        r_create_offer = requests.post(
            url=f'{settings.KEITARO_DOMAIN}/{settings.KEITARO_API_DOMAIN}/offers',
            headers=keitaro_auth.headers_with_auth(),
            json={
                'name': offer_model.name,
                'group_id': offer_model.group_id,
                'action_type': offer_model.action_type,
                'action_payload': offer_model.action_payload,
                'action_options': offer_model.action_options,
                'affiliate_network_id': affiliate_network_model.keitaro_id,
                'payout_value': offer_model.payout_value,
                'payout_currency': offer_model.payout_currency,
                'payout_type': offer_model.payout_type,
                'state': offer_model.state,
                'payout_auto': offer_model.payout_auto,
                'payout_upsell': offer_model.payout_upsell,
                'country': offer_model.country,
                'offer_type': offer_model.offer_type,
                'conversion_cap_enabled': offer_model.conversion_cap_enabled,
                'daily_cap': offer_model.daily_cap,
                'notes': offer_model.notes,
                'conversion_timezone': offer_model.conversion_timezone,
                'affiliate_network': offer_model.affiliate_network,
                'alternative_offer_id': offer_model.alternative_offer_id,
                'group': offer_model.group,
                'local_path': offer_model.local_path,
                'preview_path': offer_model.preview_path,
                'archive': str(offer_model.archive)[2:-1]
            }
        )
        if r_create_offer.status_code == 200 and r_create_offer.json() is not None:
            offer_model.keitaro_id = r_create_offer.json().get('id')
            offer_model.state = r_create_offer.json().get('state')
            self.session.commit()
            self.session.refresh(offer_model)

            return OfferOut.model_validate(offer_model)

    def get(self, offer_id: int) -> OfferOut:
        offer_model = self.session.query(Offer).filter_by(id=offer_id).one_or_none()
        return OfferOut.model_validate(offer_model)

    def keitaro_get(self, offer_id: int):
        offer_model = self.session.query(Offer).filter_by(id=offer_id).one_or_none()
        if offer_model is None:
            raise HTTPException(
                status_code=404,
                detail=f'Offer with ID {offer_id} not found'
            )

        offer_keitaro_id = offer_model.keitaro_id
        r_offer_in_keitaro = requests.get(
            url=f'{settings.KEITARO_DOMAIN}/{settings.KEITARO_API_DOMAIN}/offers/{offer_keitaro_id}',
            headers=keitaro_auth.headers_with_auth()
        )
        if r_offer_in_keitaro.status_code == 200 and r_offer_in_keitaro.json() is not None:
            offer_in_keitaro = r_offer_in_keitaro.json()
            offer_in_keitaro['keitaro_id'] = offer_in_keitaro.get('id')
            offer_in_keitaro['id'] = offer_id
            return OfferOut.model_validate(offer_in_keitaro)
