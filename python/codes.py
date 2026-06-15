from abc import ABC
from typing import Any

class BaseCode(ABC):
    """
    Абстрактный базовый класс для всех кодов ответов.
    """

    HTTPCODE: int
    CODE: str
    MESSAGE: str

class BaseErrorCode(BaseCode):
    def __init__(self, details: list[Any] | None = None):
        self.details = details


    def __str__(self):
        return f"[Error {self.CODE}]: {self.MESSAGE}, {self.details}"

class BaseOkCode(BaseCode):
    def __str__(self):
        return f"[Ok: {self.CODE}]: {self.MESSAGE}"

class HealthOK(BaseOkCode):
    HTTPCODE = 200
    CODE = "HEALTH_OK"
    MESSAGE = "Сервис жив"

class HealthError(BaseErrorCode):
    HTTPCODE = 503
    CODE = "HEALTH_ERROR"
    MESSAGE = "Сервис полумертв"

class LiveOK(BaseOkCode):
    HTTPCODE = 200
    CODE = "LIVE_OK"
    MESSAGE = "Сервис жив"

class InternalServerError(BaseErrorCode):
    HTTPCODE = 500
    CODE = "INTERNAL_SERVER_ERROR"
    MESSAGE = "Произошла ошибка при выполнении кода на сервере"

class ValidationError(BaseErrorCode):
    HTTPCODE = 422
    CODE = "4220"
    MESSAGE = "Переданы некорректные данные для обработки."
