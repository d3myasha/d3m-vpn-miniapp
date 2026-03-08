"""Исключения приложения."""

from fastapi import HTTPException, status


class AppException(HTTPException):
    """Базовое исключение приложения."""

    def __init__(
        self,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail: str = "Произошла ошибка",
    ):
        super().__init__(status_code=status_code, detail=detail)


class BadRequestException(AppException):
    """Ошибка неверного запроса."""

    def __init__(self, detail: str = "Неверный запрос"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class UnauthorizedException(AppException):
    """Ошибка авторизации."""

    def __init__(self, detail: str = "Не авторизован"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class ForbiddenException(AppException):
    """Ошибка доступа."""

    def __init__(self, detail: str = "Доступ запрещён"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class NotFoundException(AppException):
    """Ресурс не найден."""

    def __init__(self, detail: str = "Ресурс не найден"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class ConflictException(AppException):
    """Конфликт ресурсов."""

    def __init__(self, detail: str = "Конфликт ресурсов"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class RemnaWaveException(AppException):
    """Ошибка взаимодействия с RemnaWave API."""

    def __init__(self, detail: str = "Ошибка RemnaWave API"):
        super().__init__(status_code=status.HTTP_502_BAD_GATEWAY, detail=detail)
