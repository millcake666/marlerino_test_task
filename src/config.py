from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = ''
    HOST: str = ''
    PORT: str = ''
    PG_HOST: str = ''
    PG_USER: str = ''
    PG_PASSWORD: str = ''
    PG_PORT: str = ''
    PG_DATABASE: str = ''
    KEITARO_DOMAIN: str = ''
    KEITARO_API_KEY: str = ''
    KEITARO_API_DOMAIN: str = ''

    class Config:
        env_file = '../.env'

    @property
    def database_url(self):
        return f'postgresql://{self.PG_USER}:{self.PG_PASSWORD}@{self.PG_HOST}:{self.PG_PORT}/{self.PG_DATABASE}'


def get_settings():
    return Settings()
