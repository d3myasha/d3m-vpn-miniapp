"""Сервис для работы с RemnaWave API."""

import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

import httpx
from loguru import logger

from app.core.config import settings
from app.core.exceptions import RemnaWaveException


class RemnaWaveService:
    """Сервис для взаимодействия с RemnaWave API."""

    def __init__(self):
        self.base_url = settings.remnawave_base_url
        self.token = settings.remnawave_token
        self._client: Optional[httpx.AsyncClient] = None

    async def _get_client(self) -> httpx.AsyncClient:
        """Получение HTTP клиента."""
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                timeout=30.0,
                headers={
                    "Authorization": f"Bearer {self.token}",
                    "Content-Type": "application/json",
                },
            )
        return self._client

    async def close(self) -> None:
        """Закрытие клиента."""
        if self._client and not self._client.is_closed:
            await self._client.aclose()

    async def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Выполнение запроса к API."""
        client = await self._get_client()

        try:
            response = await client.request(
                method=method,
                url=endpoint,
                json=data,
                params=params,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"RemnaWave API error: {e.response.status_code} - {e.response.text}")
            raise RemnaWaveException(f"Ошибка API: {e.response.status_code}")
        except httpx.RequestError as e:
            logger.error(f"RemnaWave request error: {e}")
            raise RemnaWaveException("Ошибка соединения с RemnaWave")

    # === User Methods ===

    async def get_user(self, telegram_id: int) -> Optional[Dict[str, Any]]:
        """Получение пользователя по Telegram ID."""
        try:
            result = await self._request("GET", f"/api/users/telegram/{telegram_id}")
            return result.get("data")
        except RemnaWaveException:
            return None

    async def create_user(
        self,
        telegram_id: int,
        username: Optional[str] = None,
        name: str = "User",
    ) -> Dict[str, Any]:
        """Создание пользователя в RemnaWave."""
        data = {
            "telegramId": str(telegram_id),
            "username": username,
            "name": name,
        }
        result = await self._request("POST", "/api/users", data=data)
        return result.get("data", {})

    async def update_user(
        self,
        remna_user_id: uuid.UUID,
        data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Обновление пользователя."""
        result = await self._request("PUT", f"/api/users/{remna_user_id}", data=data)
        return result.get("data", {})

    # === Subscription Methods ===

    async def get_subscription(
        self,
        remna_user_id: uuid.UUID,
    ) -> Optional[Dict[str, Any]]:
        """Получение подписки пользователя."""
        try:
            result = await self._request(
                "GET",
                f"/api/subscriptions/user/{remna_user_id}",
            )
            return result.get("data")
        except RemnaWaveException:
            return None

    async def create_subscription(
        self,
        remna_user_id: uuid.UUID,
        plan_id: int,
        duration_days: int,
        is_trial: bool = False,
    ) -> Dict[str, Any]:
        """Создание подписки."""
        expire_at = datetime.now(timezone.utc) + timedelta(days=duration_days)

        data = {
            "userId": str(remna_user_id),
            "planId": plan_id,
            "expireAt": expire_at.isoformat(),
            "isTrial": is_trial,
        }
        result = await self._request("POST", "/api/subscriptions", data=data)
        return result.get("data", {})

    async def renew_subscription(
        self,
        subscription_id: int,
        duration_days: int,
    ) -> Dict[str, Any]:
        """Продление подписки."""
        data = {"durationDays": duration_days}
        result = await self._request(
            "POST",
            f"/api/subscriptions/{subscription_id}/renew",
            data=data,
        )
        return result.get("data", {})

    async def get_subscription_key(
        self,
        subscription_id: int,
    ) -> Dict[str, Any]:
        """Получение ключа подписки."""
        result = await self._request(
            "GET",
            f"/api/subscriptions/{subscription_id}/key",
        )
        return result.get("data", {})

    # === Device Methods ===

    async def get_devices(
        self,
        subscription_id: int,
    ) -> List[Dict[str, Any]]:
        """Получение устройств подписки."""
        result = await self._request("GET", f"/api/subscriptions/{subscription_id}/devices")
        return result.get("data", [])

    async def add_device(
        self,
        subscription_id: int,
        device_name: str,
    ) -> Dict[str, Any]:
        """Добавление устройства."""
        data = {"name": device_name}
        result = await self._request(
            "POST",
            f"/api/subscriptions/{subscription_id}/devices",
            data=data,
        )
        return result.get("data", {})

    async def remove_device(
        self,
        subscription_id: int,
        device_id: uuid.UUID,
    ) -> bool:
        """Удаление устройства."""
        await self._request(
            "DELETE",
            f"/api/subscriptions/{subscription_id}/devices/{device_id}",
        )
        return True

    async def reset_devices(
        self,
        subscription_id: int,
    ) -> bool:
        """Сброс устройств подписки."""
        await self._request(
            "POST",
            f"/api/subscriptions/{subscription_id}/devices/reset",
        )
        return True

    # === Plan Methods ===

    async def get_plans(self) -> List[Dict[str, Any]]:
        """Получение всех планов."""
        result = await self._request("GET", "/api/plans")
        return result.get("data", [])

    async def get_plan(self, plan_id: int) -> Optional[Dict[str, Any]]:
        """Получение плана по ID."""
        try:
            result = await self._request("GET", f"/api/plans/{plan_id}")
            return result.get("data")
        except RemnaWaveException:
            return None

    # === Traffic Methods ===

    async def get_traffic_usage(
        self,
        subscription_id: int,
    ) -> Dict[str, Any]:
        """Получение использования трафика."""
        result = await self._request(
            "GET",
            f"/api/subscriptions/{subscription_id}/traffic",
        )
        return result.get("data", {})


# Singleton instance
remnawave_service = RemnaWaveService()


async def get_remnawave_service() -> RemnaWaveService:
    """Получение сервиса RemnaWave."""
    return remnawave_service
