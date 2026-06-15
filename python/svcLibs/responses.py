import datetime
import uuid
from fastapi.responses import JSONResponse

from .codes import BaseOkCode, BaseErrorCode

def success_response(data, code: BaseOkCode, trace_id: str | None) -> JSONResponse:
    return JSONResponse(content={
        "data": data,
        "message": code.MESSAGE,
        "meta": {
            "code": code,
            "traceId": trace_id or uuid.uuid4().hex,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat() + "Z"
        }
    }, status_code=code.HTTPCODE)


def error_response(code: BaseErrorCode, trace_id: str | None) -> JSONResponse:
    return JSONResponse(content={
        "error": {
            "details": code.details,
            "message": code.MESSAGE,
            "code": code.CODE
        },
        "meta": {
            "traceId": trace_id or uuid.uuid4().hex,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat() + "Z"
        }
    }, status_code=code.HTTPCODE)


