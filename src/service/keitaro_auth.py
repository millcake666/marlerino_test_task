from config import get_settings


settings = get_settings()


class KeitaroAuth:
    def headers_with_auth(self) -> dict[str, str]:
        return {'Api-Key': settings.KEITARO_API_KEY}
