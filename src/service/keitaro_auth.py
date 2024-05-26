from config import get_settings


settings = get_settings()


class KeitaroAuth:
    @staticmethod
    def headers_with_auth() -> dict[str, str]:
        return {'Api-Key': settings.KEITARO_API_KEY}
