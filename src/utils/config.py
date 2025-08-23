from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MONGO_URI: str
    MONGO_DB_NAME: str

    SUPABASE_URL: str
    SUPABASE_KEY: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_EXPIRATION_MINUTES: int

    class Config:
        env_file = ".env"
        extra = "allow"


def get_settings() -> Settings:
    return Settings()
