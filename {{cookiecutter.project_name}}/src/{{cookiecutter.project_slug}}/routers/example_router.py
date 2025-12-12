from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="example")


@router.get("/ping")
def ping() -> str:
    return "pong"
