from typing import Any

from fastapi.responses import JSONResponse


def make_response(
    status_code: int = 200, status: bool = None, data: Any = None, message: str = ""
) -> JSONResponse:
    content = {
        "status": status if status is not None else status_code < 400,
        "data": data,
        "message": message,
    }
    return JSONResponse(status_code=status_code, content=content)


def bad_request(message: str = "") -> JSONResponse:
    content = {
        "status": False,
        "data": None,
        "message": message,
    }
    return JSONResponse(status_code=400, content=content)


def not_found(message: str = "") -> JSONResponse:
    content = {
        "status": False,
        "data": None,
        "message": message,
    }
    return JSONResponse(status_code=404, content=content)


def conflict(message: str = "") -> JSONResponse:
    content = {
        "status": False,
        "data": None,
        "message": message,
    }
    return JSONResponse(status_code=409, content=content)


def ok(data: Any = None, message: str = "") -> JSONResponse:
    content = {
        "status": True,
        "data": data,
        "message": message,
    }
    return JSONResponse(status_code=200, content=content)


def created(data: Any = None, message: str = "") -> JSONResponse:
    content = {
        "status": True,
        "data": data,
        "message": message,
    }
    return JSONResponse(status_code=201, content=content)
