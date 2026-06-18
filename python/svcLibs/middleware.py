import json
import logging
from typing import List, Optional
from uuid import UUID
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.middleware.base import BaseHTTPMiddleware

from responses import error_response
from .codes import InternalServerError, ValidationError

async def internal_error_handler(request: Request, exc: Exception):
    logging.getLogger("uvicorn.error").exception("Произошла внутренняя ошибка при выполнении кода на сервере", exc_info=exc)
    return error_response(InternalServerError(), request.headers.get("X-Trace-Id"))

async def validation_error_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        field = " -> ".join(str(loc) for loc in error["loc"])
        message = error["msg"]
        errors.append(f"Поле '{field}': {message}")

    logging.getLogger("uvicorn.info").warning(
        f"Ошибка валидации на URL {request.url.path}. "
        f"Детали: {', '.join(errors)}", 
        exc_info=exc
    )

    return error_response(ValidationError(errors), request.headers.get("X-Trace-Id"))

def register_errors_handlers(app: FastAPI):
    app.add_exception_handler(500, internal_error_handler)
    app.add_exception_handler(RequestValidationError, internal_error_handler)

class AuthState:
    """Удобный класс-контейнер, чтобы не работать с сырыми строками в эндпоинтах"""
    def __init__(
        self, 
        auth_type: str, 
        user_id: Optional[UUID] = None, 
        user_roles: Optional[List[str]] = None, 
        server_name: Optional[str] = None
    ):
        self.type = auth_type              # "guest", "user", "server", или "service"
        self.user_id = user_id             # UUID или None
        self.user_roles = user_roles or [] # Список ролей или пустой список
        self.server_name = server_name     # Имя сервера или None

class ParseAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        auth_type = request.headers.get("eauth-type", "guest")
        raw_user_id = request.headers.get("eauth-user-id")
        raw_roles = request.headers.get("eauth-user-roles")
        raw_server_name = request.headers.get("eauth-server-name")

        user_id = None
        server_name = None
        user_roles = []

        if auth_type == "user":
            if raw_user_id:
                try:
                    user_id = UUID(raw_user_id)
                except ValueError:
                    logging.getLogger("uvicorn.error").error(f"Не удалось распарсить user_id от gateway: {raw_user_id}")
                    return error_response(InternalServerError(), request.headers.get("X-Trace-Id"))
            
            if raw_roles:
                try:
                    user_roles = json.loads(raw_roles)
                    if not isinstance(user_roles, list):
                        user_roles = [str(user_roles)]
                except json.JSONDecodeError:
                    logging.getLogger("uvicorn.error").error(f"Не удалось распарсить user_roles от gateway: {raw_roles}")
                    return error_response(InternalServerError(), request.headers.get("X-Trace-Id"))

        elif auth_type == "server":
            server_name = raw_server_name
        elif auth_type == "guest":
            pass
        else:
            auth_type = "service"


        request.state.auth = AuthState(
            auth_type=auth_type,
            user_id=user_id,
            user_roles=user_roles,
            server_name=server_name
        )

        response = await call_next(request)
        return response

