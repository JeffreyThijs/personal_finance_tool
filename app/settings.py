from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    SECRET: str
    DATABASE_URL: PostgresDsn
    GOOGLE_OAUTH_CLIENT_ID: str
    GOOGLE_OAUTH_CLIENT_SECRET: str

    class Config:
        case_sensitive = True
        env_file = '.env'
        env_file_encoding = 'utf-8'

settings = Settings()