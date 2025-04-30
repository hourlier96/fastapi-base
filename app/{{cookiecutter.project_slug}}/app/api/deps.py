from typing import NoReturn

from fastapi import HTTPException, status
from fastapi.security import HTTPBearer

# oauth2_scheme = HTTPBearer()

def raise_400(msg: str = "Bad Request") -> NoReturn:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=msg,
    )


def raise_401(msg: str = "Not authorized") -> NoReturn:
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=msg,
    )


def raise_403(msg: str = "Not authorized") -> NoReturn:
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=msg,
    )


def raise_404(msg: str = "Not found") -> NoReturn:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=msg,
    )


def raise_500(msg: str = "Internal Server Error") -> NoReturn:
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=msg,
    )
