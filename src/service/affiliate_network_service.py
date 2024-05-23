from fastapi import HTTPException

from schemes import AffiliateNetworkIn, AffiliateNetworkOut, AffiliateNetworkState
from service import DefaultService
from config import get_settings
from service.keitaro_auth import KeitaroAuth
from database.affiliate_network import AffiliateNetwork as AffiliateNetworkModel
import requests


settings = get_settings()
keitaro_auth = KeitaroAuth()


class AffiliateNetworkService(DefaultService):
    def create(self, affiliate_network: AffiliateNetworkIn) -> AffiliateNetworkOut:
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
            model = AffiliateNetworkModel(**affiliate_network.model_dump())
            self.session.add(model)
            self.session.commit()
            self.session.refresh(model)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f'Internal server error while insert into db table AffiliateNetwork. Detail - {e}'
            )

        return AffiliateNetworkOut(**model.__dict__)

    def keitaro_create(self):
        return
        # r = requests.post(
        #     url=f'{settings.KEITARO_DOMAIN}/admin_api/v1/affiliate_networks',
        #     headers=keitaro_auth.headers_with_auth(),
        #     json=affiliate_network.model_dump()
        # )
        # # {'name': 'aff_network_test_dmitry_01_38', 'postback_url': None, 'offer_param': None, 'notes': None, 'created_at': '2024-05-22 20:38:18', 'updated_at': '2024-05-22 20:38:18', 'state': 'active', 'id': 17}
        #
        # if r.status_code == 200 and r.json() is not None:
        #     self.session.inse

    def get(self):
        return

    def keitaro_get(self):
        return
