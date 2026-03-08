import os
from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Настройки приложения."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Application
    app_domain: str = "localhost:3000"
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    app_secret_key: str
    app_crypt_key: str

    # Bot
    bot_token: str
    bot_secret_token: str
    bot_support_username: str
    bot_mini_app: bool = True

    # RemnaWave API
    remnawave_host: str
    remnawave_port: int = 443
    remnawave_token: str
    remnawave_webhook_secret: str
    remnawave_use_ssl: bool = True

    @property
    def remnawave_base_url(self) -> str:
        """Базовый URL RemnaWave API."""
        protocol = "https" if self.remnawave_use_ssl else "http"
        return f"{protocol}://{self.remnawave_host}:{self.remnawave_port}"

    # Database
    database_host: str
    database_port: int = 5432
    database_name: str
    database_user: str
    database_password: str
    database_echo: bool = False
    database_pool_size: int = 20
    database_max_overflow: int = 10
    database_pool_timeout: int = 30
    database_pool_recycle: int = 3600

    @property
    def database_url(self) -> str:
        """URL подключения к базе данных."""
        return (
            f"postgresql+asyncpg://{self.database_user}:{self.database_password}"
            f"@{self.database_host}:{self.database_port}/{self.database_name}"
        )

    # Redis
    redis_host: str
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: str

    @property
    def redis_url(self) -> str:
        """URL подключения к Redis."""
        password_part = f":{self.redis_password}@" if self.redis_password else ""
        return f"redis://{password_part}{self.redis_host}:{self.redis_port}/{self.redis_db}"

    # JWT
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30

    @property
    def origins(self) -> List[str]:
        """Разрешённые CORS origins."""
        return [
            f"https://{self.app_domain}",
            f"http://{self.app_domain}",
            "https://t.me",
            "http://t.me",
        ]


@lru_cache
def get_settings() -> Settings:
    """Получение настроек приложения (кэшируется)."""
    return Settings()


settings = get_settings()
