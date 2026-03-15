from __future__ import annotations

import html
import logging
import math
from datetime import timedelta
from typing import Any, Awaitable, Callable

from telegram import ReplyKeyboardRemove, Update
from telegram.constants import ParseMode
from telegram.error import TelegramError
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from .config import PLANS, Settings
from .db import Database, User
from .i18n import plan_label, plan_price, resolve_action, tr
from .keyboards import (
    admin_package_manage_keyboard,
    admin_users_keyboard,
    contact_admin_keyboard,
    language_keyboard,
    main_menu_keyboard,
    message_actions_keyboard,
    package_keyboard,
)
from .services import build_admin_user_tag, format_dt, next_delivery_for_plan, utc_now

logger = logging.getLogger(__name__)

SendFunc = Callable[..., Awaitable[Any]]


class ExLinksBot:
    def __init__(self, settings: Settings, db: Database):
        self.settings = settings
        self.db = db

    def build_application(self) -> Application:
        application = Application.builder().token(self.settings.bot_token).build()
        application.add_error_handler(self.error_handler)
        application.add_handler(CommandHandler("start", self.start))
        application.add_handler(CommandHandler("menu", self.show_menu_command))
        application.add_handler(CallbackQueryHandler(self.handle_callback))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_text))
        application.job_queue.run_repeating(
            self.delivery_job,
            interval=self.settings.delivery_check_seconds,
            first=10,
            name="delivery-checker",
        )
        return application

    async def error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
        logger.exception("Unhandled exception while processing update: %s", context.error)

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if update.effective_user is None or update.message is None:
            return

        self.db.upsert_user(
            telegram_id=update.effective_user.id,
            username=update.effective_user.username,
            first_name=update.effective_user.first_name,
        )
        context.user_data.clear()

        await update.message.reply_text(
            f"<b>{html.escape(self.settings.brand_name)}</b>-ə xoş gəlmisiniz.\n\n"
            "Zəhmət olmasa tətbiqə keçin:\n"
            "https://t.me/exlinks_ai_bot?startapp",
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
            reply_markup=ReplyKeyboardRemove(),
        )

    async def show_menu_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if update.effective_user is None or update.message is None:
            return

        self.db.upsert_user(
            telegram_id=update.effective_user.id,
            username=update.effective_user.username,
            first_name=update.effective_user.first_name,
        )
        await self.show_main_menu(update.message.reply_text, update.effective_user.id, context)

    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        if query is None or update.effective_user is None:
            return

        self.db.upsert_user(
            telegram_id=update.effective_user.id,
            username=update.effective_user.username,
            first_name=update.effective_user.first_name,
        )

        data = query.data or ""

        if data == "noop":
            await query.answer()
            return

        if data.startswith("lang:"):
            language = data.split(":", 1)[1]
            self.db.set_language(update.effective_user.id, language)
            context.user_data.clear()
            context.user_data["panel"] = "admin" if self.is_admin(update.effective_user.id) else "user"

            await query.answer()
            await query.edit_message_text(
                tr(language, "language_updated"),
                parse_mode=ParseMode.HTML,
            )
            await query.message.reply_text(
                tr(language, "welcome", brand=self.settings.brand_name),
                reply_markup=main_menu_keyboard(
                    language,
                    is_admin=self.is_admin(update.effective_user.id),
                    panel=context.user_data.get("panel", "user"),
                ),
                parse_mode=ParseMode.HTML,
            )
            return

        if data.startswith("plan_request:"):
            plan_code = data.split(":", 1)[1]
            language = self.get_language(update.effective_user.id)

            if plan_code not in PLANS:
                await query.answer()
                return

            context.user_data["requested_plan"] = plan_code

            await query.answer()
            await query.message.reply_text(
                tr(
                    language,
                    "plan_request",
                    plan=plan_label(language, plan_code),
                    price=plan_price(language, plan_code),
                    telegram_id=update.effective_user.id,
                ),
                parse_mode=ParseMode.HTML,
                reply_markup=contact_admin_keyboard(language),
            )
            return

        if data == "contact_admin":
            language = self.get_language(update.effective_user.id)
            plan_code = context.user_data.get("requested_plan")
            plan_text = plan_label(language, plan_code) if plan_code in PLANS else "-"

            await self.notify_admins(
                context.application,
                (
                    "💳 Package request\n"
                    f"User: {build_admin_user_tag(update.effective_user.username, update.effective_user.first_name, update.effective_user.id)}\n"
                    f"Telegram ID: {update.effective_user.id}\n"
                    f"Requested plan: {plan_text}"
                ),
            )

            await query.answer()
            await query.message.reply_text(
                tr(language, "package_request_sent"),
                parse_mode=ParseMode.HTML,
                reply_markup=main_menu_keyboard(
                    language,
                    is_admin=self.is_admin(update.effective_user.id),
                    panel=context.user_data.get("panel", "user"),
                ),
            )
            return

        if data.startswith("admin_users_page:"):
            if not self.is_admin(update.effective_user.id):
                await query.answer()
                return

            page = max(1, int(data.split(":", 1)[1]))
            language = self.get_language(update.effective_user.id)

            await query.answer()
            await self._send_users_page(query.edit_message_text, language, page)
            return

        if data.startswith("admin_user:"):
            if not self.is_admin(update.effective_user.id):
                await query.answer()
                return

            _, telegram_id_str, page_str = data.split(":", 2)
            target_id = int(telegram_id_str)
            page = max(1, int(page_str))
            language = self.get_language(update.effective_user.id)

            await query.answer()
            await self._send_user_card(query.edit_message_text, language, target_id, page)
            return

        if data.startswith("admin_set:"):
            if not self.is_admin(update.effective_user.id):
                await query.answer()
                return

            _, telegram_id_str, plan_code, page_str = data.split(":", 3)
            target_id = int(telegram_id_str)
            page = max(1, int(page_str))
            language = self.get_language(update.effective_user.id)

            if plan_code not in PLANS:
                await query.answer()
                return

            next_delivery_at = next_delivery_for_plan(plan_code)
            package_expires_at = utc_now() + timedelta(days=30)
            user = self.db.set_package(target_id, plan_code, next_delivery_at, package_expires_at)

            await query.answer()

            if user is None:
                await query.edit_message_text(tr(language, "item_not_found"), parse_mode=ParseMode.HTML)
                return

            user_lang = user.language_code or "en"
            try:
                await context.application.bot.send_message(
                    chat_id=target_id,
                    text=tr(user_lang, "package_activated_user", plan=plan_label(user_lang, plan_code)),
                    parse_mode=ParseMode.HTML,
                )
            except TelegramError:
                logger.warning("Could not notify user %s about package activation", target_id)

            try:
                await self.deliver_one_product(context.application, user)
            except Exception as exc:
                logger.exception("Immediate delivery failed for user %s: %s", target_id, exc)

            note = tr(language, "package_activated_admin", telegram_id=target_id, plan=plan_label(language, plan_code))
            await self._send_user_card(query.edit_message_text, language, target_id, page, note=note)
            return

        if data.startswith("admin_deactivate:"):
            if not self.is_admin(update.effective_user.id):
                await query.answer()
                return

            _, telegram_id_str, page_str = data.split(":", 2)
            target_id = int(telegram_id_str)
            page = max(1, int(page_str))
            language = self.get_language(update.effective_user.id)

            user = self.db.deactivate_package(target_id)

            await query.answer()

            if user is None:
                await query.edit_message_text(tr(language, "item_not_found"), parse_mode=ParseMode.HTML)
                return

            user_lang = user.language_code or "en"
            try:
                await context.application.bot.send_message(
                    chat_id=target_id,
                    text=tr(user_lang, "package_deactivated_user"),
                    parse_mode=ParseMode.HTML,
                )
            except TelegramError:
                logger.warning("Could not notify user %s about package deactivation", target_id)

            note = tr(language, "package_deactivated_admin", telegram_id=target_id)
            await self._send_user_card(query.edit_message_text, language, target_id, page, note=note)
            return

        if data.startswith("message_reply:"):
            if not self.is_admin(update.effective_user.id):
                await query.answer()
                return

            _, kind, item_id_str = data.split(":", 2)
            item_id = int(item_id_str)
            language = self.get_language(update.effective_user.id)

            context.user_data["pending_action"] = "reply_message"
            context.user_data["reply_message_kind"] = kind
            context.user_data["reply_message_id"] = item_id

            await query.answer()
            await query.message.reply_text(
                tr(language, "reply_prompt_message"),
                parse_mode=ParseMode.HTML,
            )
            return

        if data.startswith("message_delete:"):
            if not self.is_admin(update.effective_user.id):
                await query.answer()
                return

            _, kind, item_id_str = data.split(":", 2)
            item_id = int(item_id_str)
            language = self.get_language(update.effective_user.id)
            ok = self.db.delete_message_item(kind, item_id)

            await query.answer()
            await query.edit_message_text(
                tr(language, "message_deleted" if ok else "item_not_found"),
                parse_mode=ParseMode.HTML,
            )
            return

        await query.answer()

    async def handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if update.effective_user is None or update.message is None or not update.message.text:
            return

        self.db.upsert_user(
            telegram_id=update.effective_user.id,
            username=update.effective_user.username,
            first_name=update.effective_user.first_name,
        )

        telegram_id = update.effective_user.id
        language = self.get_language(telegram_id)
        text = update.message.text.strip()

        pending_action = context.user_data.get("pending_action")

        if pending_action == "contact":
            self.db.add_review(telegram_id, text)
            context.user_data.pop("pending_action", None)

            await self.notify_admins(
                context.application,
                (
                    "💬 New message\n"
                    f"From: {build_admin_user_tag(update.effective_user.username, update.effective_user.first_name, telegram_id)}\n"
                    f"Telegram ID: {telegram_id}\n\n{text}"
                ),
            )

            await update.message.reply_text(
                tr(language, "message_sent"),
                reply_markup=main_menu_keyboard(
                    language,
                    self.is_admin(telegram_id),
                    context.user_data.get("panel", "user"),
                ),
                parse_mode=ParseMode.HTML,
            )
            return

        if pending_action == "reply_message":
            if not self.is_admin(telegram_id):
                context.user_data.pop("pending_action", None)
                context.user_data.pop("reply_message_id", None)
                context.user_data.pop("reply_message_kind", None)
                await update.message.reply_text(tr(language, "admin_only"), parse_mode=ParseMode.HTML)
                return

            item_id = context.user_data.get("reply_message_id")
            kind = context.user_data.get("reply_message_kind")

            item, user = self.db.get_message_item(kind, item_id) if item_id and kind else (None, None)
            if item is None or user is None:
                context.user_data.pop("pending_action", None)
                context.user_data.pop("reply_message_id", None)
                context.user_data.pop("reply_message_kind", None)
                await update.message.reply_text(tr(language, "item_not_found"), parse_mode=ParseMode.HTML)
                return

            user_lang = user.language_code or "en"
            try:
                await context.application.bot.send_message(
                    chat_id=user.telegram_id,
                    text=tr(user_lang, "message_reply_user", text=html.escape(text)),
                    parse_mode=ParseMode.HTML,
                )
            except TelegramError:
                await update.message.reply_text(tr(language, "item_not_found"), parse_mode=ParseMode.HTML)
                return

            if kind == "complaint":
                self.db.set_complaint_status(item_id, "answered")

            context.user_data.pop("pending_action", None)
            context.user_data.pop("reply_message_id", None)
            context.user_data.pop("reply_message_kind", None)
            await update.message.reply_text(tr(language, "reply_sent"), parse_mode=ParseMode.HTML)
            return

        if pending_action == "broadcast":
            if not self.is_admin(telegram_id):
                context.user_data.pop("pending_action", None)
                await update.message.reply_text(tr(language, "admin_only"), parse_mode=ParseMode.HTML)
                return

            context.user_data.pop("pending_action", None)
            success = 0
            failed = 0

            for chat_id in self.db.get_all_user_chat_ids():
                try:
                    await context.application.bot.send_message(chat_id=chat_id, text=text)
                    success += 1
                except TelegramError:
                    failed += 1

            await update.message.reply_text(
                tr(language, "broadcast_done", success=success, failed=failed),
                reply_markup=main_menu_keyboard(language, True, context.user_data.get("panel", "admin")),
                parse_mode=ParseMode.HTML,
            )
            return

        action = resolve_action(text)

        if action is None:
            await update.message.reply_text(
                tr(language, "unknown_message"),
                reply_markup=main_menu_keyboard(
                    language,
                    self.is_admin(telegram_id),
                    context.user_data.get("panel", "admin" if self.is_admin(telegram_id) else "user"),
                ),
                parse_mode=ParseMode.HTML,
            )
            return

        if action == "packages":
            await update.message.reply_text(
                tr(language, "packages_title"),
                reply_markup=package_keyboard(language),
                parse_mode=ParseMode.HTML,
            )
            return

        if action == "subscription":
            user = self.db.get_user(telegram_id)
            if user is None or not user.package_active or not user.package_code:
                await update.message.reply_text(tr(language, "subscription_none"), parse_mode=ParseMode.HTML)
                return

            remaining = self.db.count_remaining_products(user.id)
            await update.message.reply_text(
                tr(
                    language,
                    "subscription_active",
                    plan=plan_label(language, user.package_code),
                    price=plan_price(language, user.package_code),
                    started=format_dt(user.package_started_at),
                    expires=format_dt(user.package_expires_at),
                    next_delivery=format_dt(user.next_delivery_at),
                    remaining=remaining,
                ),
                parse_mode=ParseMode.HTML,
            )
            return

        if action in {"contact", "review", "support"}:
            context.user_data["pending_action"] = "contact"
            await update.message.reply_text(
                tr(language, "contact_prompt"),
                parse_mode=ParseMode.HTML,
            )
            return

        if action == "change_language":
            await update.message.reply_text(
                tr(language, "choose_language", brand=self.settings.brand_name),
                reply_markup=language_keyboard(),
                parse_mode=ParseMode.HTML,
            )
            return

        if action == "switch_user" and self.is_admin(telegram_id):
            context.user_data["panel"] = "user"
            await update.message.reply_text(
                tr(language, "welcome", brand=self.settings.brand_name),
                reply_markup=main_menu_keyboard(language, True, "user"),
                parse_mode=ParseMode.HTML,
            )
            return

        if action == "switch_admin" and self.is_admin(telegram_id):
            context.user_data["panel"] = "admin"
            await update.message.reply_text(
                tr(language, "welcome", brand=self.settings.brand_name),
                reply_markup=main_menu_keyboard(language, True, "admin"),
                parse_mode=ParseMode.HTML,
            )
            return

        if not self.is_admin(telegram_id):
            await update.message.reply_text(tr(language, "admin_only"), parse_mode=ParseMode.HTML)
            return

        if action == "admin_users":
            await self._send_users_page(update.message.reply_text, language, page=1)
            return

        if action == "admin_broadcast":
            context.user_data["pending_action"] = "broadcast"
            await update.message.reply_text(tr(language, "broadcast_prompt"), parse_mode=ParseMode.HTML)
            return

        if action in {"admin_messages", "admin_reviews", "admin_complaints"}:
            items = self.db.latest_all_messages(limit=20)
            if not items:
                await update.message.reply_text(tr(language, "list_empty"), parse_mode=ParseMode.HTML)
                return

            for item in items:
                user = item["user"]
                name = self._user_display_name(user)
                telegram_value = user.telegram_id if user is not None else "-"

                await update.message.reply_text(
                    tr(
                        language,
                        "admin_message_detail",
                        name=html.escape(name),
                        telegram_id=telegram_value,
                        date=format_dt(item["created_at"]),
                        text=html.escape(item["text"]),
                    ),
                    parse_mode=ParseMode.HTML,
                    reply_markup=message_actions_keyboard(
                        language,
                        item["id"],
                        kind=item["kind"],
                        can_reply=user is not None,
                    ),
                )
            return

    async def delivery_job(self, context: ContextTypes.DEFAULT_TYPE) -> None:
        now = utc_now()

        expired_users = self.db.get_expired_users(now)
        for user in expired_users:
            try:
                self.db.deactivate_package(user.telegram_id)

                language = user.language_code or "en"
                try:
                    await context.application.bot.send_message(
                        chat_id=user.telegram_id,
                        text=tr(language, "package_expired_user"),
                        parse_mode=ParseMode.HTML,
                    )
                except TelegramError:
                    logger.warning("Could not notify user %s about package expiry", user.telegram_id)

                await self.notify_admins(
                    context.application,
                    tr("az", "package_expired_admin", telegram_id=user.telegram_id),
                )
            except Exception as exc:
                logger.exception("Expiry processing failed for user %s: %s", user.telegram_id, exc)

        due_users = self.db.get_due_users(now)

        for user in due_users:
            try:
                await self.deliver_one_product(context.application, user)
            except Exception as exc:
                logger.exception("Delivery job failed for user %s: %s", user.telegram_id, exc)

    async def deliver_one_product(self, application: Application, user: User) -> None:
        language = user.language_code or "en"
        if not user.package_code or not user.package_active:
            return

        product = self.db.get_random_unsent_product(user.id)
        next_delivery_at = next_delivery_for_plan(user.package_code)

        if product is None:
            active_products = self.db.get_stats()["active_products"]
            text_key = "catalog_empty" if active_products == 0 else "no_more_products"
            try:
                await application.bot.send_message(
                    chat_id=user.telegram_id,
                    text=tr(language, text_key),
                    parse_mode=ParseMode.HTML,
                )
            except TelegramError:
                logger.warning("Could not send empty-catalog notice to %s", user.telegram_id)

            self.db.update_next_delivery(user.id, next_delivery_at)
            return

        safe_name = html.escape(product.name)
        safe_link = html.escape(product.link)

        try:
            await application.bot.send_message(
                chat_id=user.telegram_id,
                text=tr(language, "new_product", name=safe_name, link=safe_link),
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=False,
            )
            self.db.add_delivery(user.id, product.id)
        except TelegramError:
            logger.warning("Could not deliver product to user %s", user.telegram_id)
        finally:
            self.db.update_next_delivery(user.id, next_delivery_at)

    def is_admin(self, telegram_id: int) -> bool:
        return telegram_id in self.settings.admin_ids

    def get_language(self, telegram_id: int) -> str:
        user = self.db.get_user(telegram_id)
        if user and user.language_code:
            return user.language_code
        return "en"

    async def show_main_menu(self, reply_func: SendFunc, telegram_id: int, context: ContextTypes.DEFAULT_TYPE) -> None:
        language = self.get_language(telegram_id)
        panel = context.user_data.get("panel") or ("admin" if self.is_admin(telegram_id) else "user")
        context.user_data["panel"] = panel

        await reply_func(
            tr(language, "welcome", brand=self.settings.brand_name),
            reply_markup=main_menu_keyboard(language, self.is_admin(telegram_id), panel),
            parse_mode=ParseMode.HTML,
        )

    async def notify_admins(self, application: Application, text: str) -> None:
        sent_targets: set[int] = set()

        if self.settings.support_chat_id:
            try:
                await application.bot.send_message(chat_id=self.settings.support_chat_id, text=text)
                sent_targets.add(self.settings.support_chat_id)
            except TelegramError:
                logger.warning("Failed to notify support chat %s", self.settings.support_chat_id)

        for admin_id in self.settings.admin_ids:
            if admin_id in sent_targets:
                continue
            try:
                await application.bot.send_message(chat_id=admin_id, text=text, parse_mode=ParseMode.HTML)
            except TelegramError:
                logger.warning("Failed to notify admin %s", admin_id)

    async def _send_users_page(self, send_func: SendFunc, language: str, page: int = 1) -> None:
        users, total = self.db.get_users_paginated(page=page, per_page=10)
        pages = max(1, math.ceil(total / 10))
        stats = self.db.get_stats()

        await send_func(
            tr(
                language,
                "user_list_title",
                page=page,
                pages=pages,
                total_users=stats["total_users"],
                active_subscriptions=stats["active_subscriptions"],
            ),
            parse_mode=ParseMode.HTML,
            reply_markup=admin_users_keyboard(language, users, page, total, 10),
        )

    async def _send_user_card(
        self,
        send_func: SendFunc,
        language: str,
        telegram_id: int,
        page: int = 1,
        note: str | None = None,
    ) -> None:
        user = self.db.get_user_by_telegram_id(telegram_id)
        if user is None:
            await send_func(tr(language, "item_not_found"), parse_mode=ParseMode.HTML)
            return

        name = html.escape(self._user_display_name(user))
        package = plan_label(language, user.package_code) if user.package_code else "-"
        status = tr(language, "status_active") if user.package_active else tr(language, "status_inactive")

        card = tr(
            language,
            "user_card",
            name=name,
            telegram_id=user.telegram_id,
            language=html.escape(user.language_code or "en"),
            package=html.escape(package),
            status=html.escape(status),
        )
        text = f"{note}\n\n{card}" if note else card

        await send_func(
            text,
            parse_mode=ParseMode.HTML,
            reply_markup=admin_package_manage_keyboard(language, user.telegram_id, page),
        )

    def _user_display_name(self, user: User | None) -> str:
        if user is None:
            return "Unknown"
        return build_admin_user_tag(user.username, user.first_name, user.telegram_id)
