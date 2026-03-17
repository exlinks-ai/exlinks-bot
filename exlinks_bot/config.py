from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

load_dotenv(BASE_DIR / ".env")


def _normalize_database_url(raw: str) -> str:
    if raw.startswith("postgres://"):
        return raw.replace("postgres://", "postgresql+psycopg://", 1)
    if raw.startswith("postgresql://") and "+psycopg" not in raw:
        return raw.replace("postgresql://", "postgresql+psycopg://", 1)
    return raw


def _parse_admin_ids(raw: str) -> set[int]:
    ids: set[int] = set()
    for chunk in raw.split(","):
        value = chunk.strip()
        if value.isdigit():
            ids.add(int(value))
    return ids


def _parse_optional_int(raw: str) -> int | None:
    value = raw.strip()
    if not value:
        return None
    try:
        return int(value)
    except ValueError:
        return None


@dataclass(frozen=True)
class Settings:
    bot_token: str
    admin_ids: set[int]
    support_chat_id: int | None
    database_url: str
    brand_name: str
    delivery_check_seconds: int
    startapp_url: str
    miniapp_url: str


PLANS: dict[str, dict[str, object]] = {
    "every_3_days": {
        "days": 3,
        "prices": {
            "az": "14.99 AZN",
            "en": "8.99$",
            "ru": "799₽",
        },
    },
    "every_2_days": {
        "days": 2,
        "prices": {
            "az": "24.99 AZN",
            "en": "14.99$",
            "ru": "1299₽",
        },
    },
    "daily": {
        "days": 1,
        "prices": {
            "az": "39.99 AZN",
            "en": "23.99$",
            "ru": "1999₽",
        },
    },
}


DEFAULT_DATABASE_URL = f"sqlite:///{(DATA_DIR / 'bot.db').as_posix()}"


settings = Settings(
    bot_token=os.getenv("BOT_TOKEN", ""),
    admin_ids=_parse_admin_ids(os.getenv("ADMIN_IDS", "")),
    support_chat_id=_parse_optional_int(os.getenv("SUPPORT_CHAT_ID", "")),
    database_url=_normalize_database_url(
        os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL)
    ),
    brand_name=os.getenv("BRAND_NAME", "exlinks.ai"),
    delivery_check_seconds=max(15, int(os.getenv("DELIVERY_CHECK_SECONDS", "60"))),
    startapp_url=os.getenv("STARTAPP_URL", "https://t.me/exlinks_ai_bot?startapp"),
    miniapp_url=os.getenv("MINIAPP_URL", "https://exlinks-web.onrender.com/miniapp"),
)
