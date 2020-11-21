from pydantic import BaseSettings, PostgresDsn, EmailStr
from fastapi_mail import ConnectionConfig


class MailSettings(ConnectionConfig):
    class Config:
        case_sensitive = True
        env_file = '.env'
        env_file_encoding = 'utf-8'


class Settings(BaseSettings):
    SECRET: str
    DATABASE_URL: PostgresDsn
    GOOGLE_OAUTH_CLIENT_ID: str
    GOOGLE_OAUTH_CLIENT_SECRET: str
    MAIL_PORT: int = 587
    MAIL_TLS: bool = True
    MAIL_SSL: bool = False

    class Config:
        case_sensitive = True
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
mail_settings = MailSettings()
