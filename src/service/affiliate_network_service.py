from fastapi import HTTPException

from schemes import AffiliateNetworkIn, AffiliateNetworkOut, AffiliateNetworkOutFull
from service import DefaultService
from config import get_settings
from service.keitaro_auth import KeitaroAuth
from database import AffiliateNetwork, User, UserToAffiliateNetwork
import requests

settings = get_settings()
keitaro_auth = KeitaroAuth()


class AffiliateNetworkService(DefaultService):
    def create(self, user_id: int, affiliate_network: AffiliateNetworkIn) -> AffiliateNetworkOut:
        exist_affiliate_networks = requests.get(
            url=f'{settings.KEITARO_DOMAIN}/{settings.KEITARO_API_DOMAIN}/affiliate_networks',
            headers=keitaro_auth.headers_with_auth()
        )

        if exist_affiliate_networks.status_code == 200 and exist_affiliate_networks.json() is not None:
            for exist_affiliate_network in exist_affiliate_networks.json():
                exist_affiliate_network: dict

                exist_affiliate_network_name = exist_affiliate_network.get('name')
                if exist_affiliate_network_name is not None and exist_affiliate_network_name == affiliate_network.name:
                    raise HTTPException(status_code=422,
                                        detail=f'Affiliate network with name '
                                               f'"{affiliate_network.name}" is already exist')
        else:
            raise HTTPException(status_code=500,
                                detail='Error while adding affiliate network')

        try:
            affiliate_network_model = AffiliateNetwork(**affiliate_network.model_dump())
            self.session.add(affiliate_network_model)
            self.session.commit()
            self.session.refresh(affiliate_network_model)

            model_link = UserToAffiliateNetwork(
                user_id=user_id,
                affiliate_network_id=affiliate_network_model.id
            )
            self.session.add(model_link)
            self.session.commit()

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f'Internal server error while insert into db table AffiliateNetwork. Detail - {e}'
            )

        return AffiliateNetworkOut.model_validate(affiliate_network_model)

    def keitaro_create(self, user_id: int, affiliate_network_id: int) -> AffiliateNetworkOut:
        user = self.session.query(User).filter_by(id=user_id).one_or_none()

        if user is None:
            raise HTTPException(
                status_code=404,
                detail=f'User not found. The user with ID {user_id} does not exist.'
            )

        for user_affiliate_network in user.affiliate_networks:
            user_affiliate_network: AffiliateNetwork

            if user_affiliate_network.id == affiliate_network_id:
                r = requests.post(
                    url=f'{settings.KEITARO_DOMAIN}/admin_api/v1/affiliate_networks',
                    headers=keitaro_auth.headers_with_auth(),
                    json={
                        'name': user_affiliate_network.name,
                        'postback_url': user_affiliate_network.postback_url,
                        'offer_param': user_affiliate_network.offer_param,
                        'notes': user_affiliate_network.notes
                    }
                )

                if r.status_code == 200 and r.json() is not None:
                    user_affiliate_network.keitaro_id = r.json().get('id')
                    user_affiliate_network.state = r.json().get('state')
                    self.session.commit()
                    self.session.refresh(user_affiliate_network)

                    return AffiliateNetworkOut.model_validate(user_affiliate_network)

    def get(self, affiliate_network_id: int) -> AffiliateNetworkOut:
        try:
            affiliate_network = self.session.query(AffiliateNetwork).filter_by(id=affiliate_network_id).one_or_none()

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f'Internal server error while getting from db table AffiliateNetwork. Detail - {e}'
            )

        if affiliate_network is None:
            raise HTTPException(
                status_code=404,
                detail=f'AffiliateNetwork not found. '
                       f'The affiliate network with ID {affiliate_network_id} does not exist.'
            )

        return AffiliateNetworkOut.model_validate(affiliate_network)

    def keitaro_get(self, affiliate_network_id: int) -> AffiliateNetworkOutFull:
        affiliate_network = self.session.query(AffiliateNetwork).filter_by(
            id=affiliate_network_id
        ).one_or_none()

        if affiliate_network is None:
            raise HTTPException(
                status_code=404,
                detail=f'AffiliateNetwork not found. '
                       f'The affiliate network with ID {affiliate_network_id} does not exist.'
            )

        if affiliate_network.keitaro_id is None:
            raise HTTPException(
                status_code=400,
                detail=f'The affiliate network with ID {affiliate_network_id} was not created in Keitaro.'
            )

        r = requests.get(f'{settings.KEITARO_DOMAIN}/admin_api/v1/affiliate_networks/{affiliate_network.keitaro_id}',
                         headers=keitaro_auth.headers_with_auth())

        if r.status_code == 200 and r.json() is not None:
            affiliate_network_data = r.json()
            affiliate_network_data['keitaro_id'] = affiliate_network_data.get('id')
            affiliate_network_data['id'] = affiliate_network_id
            return AffiliateNetworkOutFull.model_validate(affiliate_network_data)

        else:
            raise HTTPException(status_code=500, detail='Failed to get response from Keitaro API')
