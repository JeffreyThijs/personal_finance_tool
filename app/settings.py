from pydantic import BaseSettings, PostgresDsn, EmailStr, validator
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
    MIN_DB_SESSIONS: int = 2
    MAX_DB_SESSIONS: int = 5
    MAIL_PORT: int = 587
    MAIL_TLS: bool = True
    MAIL_SSL: bool = False

    class Config:
        case_sensitive = True
        env_file = '.env'
        env_file_encoding = 'utf-8'

    @validator('MIN_DB_SESSIONS', always=True)
    def min_db_session_check(cls, v, values, **kwargs):
        if 'MAX_DB_SESSIONS' in values and v > values['MAX_DB_SESSIONS']:
            raise ValueError("MIN_DB_SESSIONS can't be higher than MAX_DB_SESSIONS")
        return v

    @validator('MAX_DB_SESSIONS', always=True)
    def max_db_session_check(cls, v, values, **kwargs):
        if 'MIN_DB_SESSIONS' in values and v < values['MIN_DB_SESSIONS']:
            raise ValueError("MAX_DB_SESSIONS can't be lower than MIN_DB_SESSIONS")
        return v


settings = Settings()
mail_settings = MailSettings()
