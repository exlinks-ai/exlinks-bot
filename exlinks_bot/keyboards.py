from __future__ import annotations

import math

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

from .i18n import LANGUAGES, button, plan_label, plan_price, tr


def language_keyboard() -> InlineKeyboardMarkup:
    rows = [[InlineKeyboardButton(title, callback_data=f"lang:{code}")] for code, title in LANGUAGES.items()]
    return InlineKeyboardMarkup(rows)


def package_keyboard(lang: str) -> InlineKeyboardMarkup:
    rows = []
    for code in ("every_3_days", "every_2_days", "daily"):
        text = f"{plan_label(lang, code)} — {plan_price(lang, code)}"
        rows.append([InlineKeyboardButton(text, callback_data=f"plan_request:{code}")])
    return InlineKeyboardMarkup(rows)


def main_menu_keyboard(lang: str, is_admin: bool, panel: str) -> ReplyKeyboardMarkup:
    if is_admin and panel == "admin":
        keyboard = [
            [button(lang, "admin_users"), button(lang, "admin_broadcast")],
            [button(lang, "admin_messages")],
            [button(lang, "switch_user")],
        ]
    else:
        keyboard = [
            [button(lang, "packages"), button(lang, "subscription")],
            [button(lang, "contact")],
            [button(lang, "change_language")],
        ]
        if is_admin:
            keyboard.append([button(lang, "switch_admin")])

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        is_persistent=True,
    )


def contact_admin_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(button(lang, "contact_admin"), callback_data="contact_admin")]]
    )


def admin_package_manage_keyboard(lang: str, telegram_id: int, page: int = 1) -> InlineKeyboardMarkup:
    rows = [
        [
            InlineKeyboardButton(
                f"{plan_label(lang, 'every_3_days')} — {plan_price(lang, 'every_3_days')}",
                callback_data=f"admin_set:{telegram_id}:every_3_days:{page}",
            )
        ],
        [
            InlineKeyboardButton(
                f"{plan_label(lang, 'every_2_days')} — {plan_price(lang, 'every_2_days')}",
                callback_data=f"admin_set:{telegram_id}:every_2_days:{page}",
            )
        ],
        [
            InlineKeyboardButton(
                f"{plan_label(lang, 'daily')} — {plan_price(lang, 'daily')}",
                callback_data=f"admin_set:{telegram_id}:daily:{page}",
            )
        ],
        [
            InlineKeyboardButton(
                button(lang, "deactivate_package"),
                callback_data=f"admin_deactivate:{telegram_id}:{page}",
            )
        ],
        [InlineKeyboardButton(button(lang, "back_to_users"), callback_data=f"admin_users_page:{page}")],
    ]
    return InlineKeyboardMarkup(rows)


def admin_users_keyboard(lang: str, users: list, page: int, total: int, per_page: int = 10) -> InlineKeyboardMarkup:
    rows: list[list[InlineKeyboardButton]] = []

    for user in users:
        name = (user.first_name or user.username or str(user.telegram_id)).strip()
        package = plan_label(lang, user.package_code) if user.package_code else "-"
        status = tr(lang, "status_active") if user.package_active else tr(lang, "status_inactive")
        text = f"{name} | {package} | {status}"
        if len(text) > 60:
            text = text[:57] + "..."
        rows.append([InlineKeyboardButton(text, callback_data=f"admin_user:{user.telegram_id}:{page}")])

    total_pages = max(1, math.ceil(total / per_page))
    nav: list[InlineKeyboardButton] = []
    if page > 1:
        nav.append(InlineKeyboardButton("⬅️", callback_data=f"admin_users_page:{page - 1}"))
    nav.append(InlineKeyboardButton(f"{page}/{total_pages}", callback_data="noop"))
    if page < total_pages:
        nav.append(InlineKeyboardButton("➡️", callback_data=f"admin_users_page:{page + 1}"))
    if nav:
        rows.append(nav)

    return InlineKeyboardMarkup(rows)


def message_actions_keyboard(lang: str, item_id: int, kind: str = "message", can_reply: bool = True) -> InlineKeyboardMarkup:
    row: list[InlineKeyboardButton] = []
    if can_reply:
        row.append(InlineKeyboardButton(button(lang, "reply_item"), callback_data=f"message_reply:{kind}:{item_id}"))
    row.append(InlineKeyboardButton(button(lang, "delete_item"), callback_data=f"message_delete:{kind}:{item_id}"))
    return InlineKeyboardMarkup([row])


# Köhnə funksiyalar saxlanılır ki, bot.py hələ dəyişməyibsə xəta verməsin
def review_actions_keyboard(lang: str, review_id: int, can_reply: bool = True) -> InlineKeyboardMarkup:
    row: list[InlineKeyboardButton] = []
    if can_reply:
        row.append(InlineKeyboardButton(button(lang, "reply_item"), callback_data=f"review_reply:{review_id}"))
    row.append(InlineKeyboardButton(button(lang, "delete_item"), callback_data=f"review_delete:{review_id}"))
    return InlineKeyboardMarkup([row])


def complaint_actions_keyboard(lang: str, complaint_id: int, can_reply: bool = True) -> InlineKeyboardMarkup:
    row: list[InlineKeyboardButton] = []
    if can_reply:
        row.append(InlineKeyboardButton(button(lang, "reply_item"), callback_data=f"complaint_reply:{complaint_id}"))
    row.append(InlineKeyboardButton(button(lang, "delete_item"), callback_data=f"complaint_delete:{complaint_id}"))
    return InlineKeyboardMarkup([row])