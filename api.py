from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlalchemy import select

from exlinks_bot.config import PLANS, settings
from exlinks_bot.db import Database, Delivery, Product, User
from exlinks_bot.i18n import LANGUAGES, plan_label, plan_price
from exlinks_bot.services import format_dt, next_delivery_for_plan

app = FastAPI(title="ExLinks Mini App API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = Database(settings.database_url)
db.init_db()

MINIAPP_DIR = Path("exlinks_miniapp")
if MINIAPP_DIR.exists():
    app.mount("/miniapp", StaticFiles(directory=str(MINIAPP_DIR), html=True), name="miniapp")


class SetLanguagePayload(BaseModel):
    telegram_id: int
    language: str


class ContactPayload(BaseModel):
    telegram_id: int
    text: str


class AdminPackagePayload(BaseModel):
    admin_telegram_id: int
    target_telegram_id: int
    package_code: str | None = None
    deactivate: bool = False


@app.get("/api/health")
def health() -> dict:
    return {"ok": True}


@app.get("/api/bootstrap")
def bootstrap(
    telegram_id: int = Query(...),
    username: str | None = Query(None),
    first_name: str | None = Query(None),
) -> dict:
    user = db.get_user_by_telegram_id(telegram_id)

    if user is None:
        user = db.upsert_user(
            telegram_id=telegram_id,
            username=username,
            first_name=first_name,
        )

    language = user.language_code if user.language_code in LANGUAGES else "en"
    is_admin = telegram_id in settings.admin_ids

    latest_or_next = _get_latest_or_next_product(user)

    plans = [
        {
            "code": code,
            "label": plan_label(language, code),
            "price": plan_price(language, code),
            "days": int(PLANS[code]["days"]),
        }
        for code in ("every_3_days", "every_2_days", "daily")
    ]

    payload = {
        "user": {
            "telegram_id": user.telegram_id,
            "username": user.username,
            "first_name": user.first_name,
            "language": language,
            "is_admin": is_admin,
        },
        "subscription": {
            "active": bool(user.package_active),
            "code": user.package_code,
            "name": plan_label(language, user.package_code) if user.package_code else "-",
            "price": plan_price(language, user.package_code) if user.package_code else "-",
            "started_at": format_dt(user.package_started_at),
            "next_delivery": format_dt(user.next_delivery_at),
        },
        "plans": plans,
        "product": latest_or_next,
    }

    if is_admin:
        payload["admin"] = {
            "users": _admin_users(language),
            "messages": _admin_messages(),
        }

    return payload


@app.post("/api/set-language")
def set_language(payload: SetLanguagePayload) -> dict:
    if payload.language not in LANGUAGES:
        raise HTTPException(status_code=400, detail="Invalid language")

    db.set_language(payload.telegram_id, payload.language)
    return {"ok": True}


@app.post("/api/contact")
def contact(payload: ContactPayload) -> dict:
    if not payload.text.strip():
        raise HTTPException(status_code=400, detail="Empty message")

    db.add_review(payload.telegram_id, payload.text.strip())
    return {"ok": True}


@app.post("/api/admin/package")
def admin_package(payload: AdminPackagePayload) -> dict:
    if payload.admin_telegram_id not in settings.admin_ids:
        raise HTTPException(status_code=403, detail="Admin only")

    target = db.get_user_by_telegram_id(payload.target_telegram_id)
    if target is None:
        raise HTTPException(status_code=404, detail="User not found")

    if payload.deactivate:
        db.deactivate_package(payload.target_telegram_id)
        return {"ok": True, "status": "deactivated"}

    if payload.package_code not in PLANS:
        raise HTTPException(status_code=400, detail="Invalid package code")

    next_delivery = next_delivery_for_plan(payload.package_code)
    db.set_package(payload.target_telegram_id, payload.package_code, next_delivery)
    return {"ok": True, "status": "activated"}


@app.get("/api/me")
def get_me(
    telegram_id: int = Query(...),
    username: str | None = Query(None),
    first_name: str | None = Query(None),
) -> dict:
    user = db.get_user_by_telegram_id(telegram_id)

    if user is None:
        user = db.upsert_user(
            telegram_id=telegram_id,
            username=username,
            first_name=first_name,
        )

    language = user.language_code if user.language_code in LANGUAGES else "en"
    latest_or_next = _get_latest_or_next_product(user)

    plans = [
        {
            "code": code,
            "label": plan_label(language, code),
            "price": plan_price(language, code),
            "days": int(PLANS[code]["days"]),
        }
        for code in ("every_3_days", "every_2_days", "daily")
    ]

    return {
        "user": {
            "telegram_id": user.telegram_id,
            "username": user.username,
            "first_name": user.first_name,
            "language": language,
            "is_admin": telegram_id in settings.admin_ids,
        },
        "subscription": {
            "active": bool(user.package_active),
            "code": user.package_code,
            "name": plan_label(language, user.package_code) if user.package_code else "-",
            "price": plan_price(language, user.package_code) if user.package_code else "-",
            "started_at": format_dt(user.package_started_at),
            "next_delivery": format_dt(user.next_delivery_at),
        },
        "plans": plans,
        "product": latest_or_next,
    }


@app.get("/")
def root():
    index_file = MINIAPP_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return {"message": "ExLinks API is running"}


def _get_latest_or_next_product(user: User) -> dict:
    if not user.package_active or not user.package_code:
        return {
            "mode": "locked",
            "name": "",
            "link": "",
            "status": "waiting",
        }

    with db.session() as session:
        latest_delivery = session.execute(
            select(Delivery, Product)
            .join(Product, Delivery.product_id == Product.id)
            .where(Delivery.user_id == user.id)
            .order_by(Delivery.sent_at.desc())
            .limit(1)
        ).first()

        if latest_delivery is not None:
            _, product = latest_delivery
            return {
                "mode": "latest",
                "name": product.name,
                "link": product.link,
                "status": "ready",
            }

        delivered_subquery = select(Delivery.product_id).where(Delivery.user_id == user.id)
        next_product = session.scalar(
            select(Product)
            .where(Product.is_active.is_(True), Product.id.not_in(delivered_subquery))
            .limit(1)
        )

        if next_product is not None:
            return {
                "mode": "next",
                "name": next_product.name,
                "link": next_product.link,
                "status": "ready",
            }

    return {
        "mode": "empty",
        "name": "No product yet",
        "link": "#",
        "status": "waiting",
    }


def _admin_users(language: str) -> list[dict]:
    users, _ = db.get_users_paginated(page=1, per_page=50)
    result = []

    for user in users:
        result.append(
            {
                "telegram_id": user.telegram_id,
                "name": user.first_name or user.username or f"User {user.telegram_id}",
                "language": user.language_code or "en",
                "package_code": user.package_code,
                "package_name": plan_label(language, user.package_code) if user.package_code else "-",
                "active": bool(user.package_active),
                "next_delivery": format_dt(user.next_delivery_at),
            }
        )

    return result


def _admin_messages() -> list[dict]:
    items = db.latest_all_messages(limit=50)
    result = []

    for item in items:
        user = item["user"]
        result.append(
            {
                "kind": item["kind"],
                "id": item["id"],
                "text": item["text"],
                "created_at": format_dt(item["created_at"]),
                "user_name": (
                    user.first_name if user and user.first_name
                    else (user.username if user and user.username else "Unknown")
                ),
                "telegram_id": user.telegram_id if user else "-",
            }
        )

    return result
