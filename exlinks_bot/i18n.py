from __future__ import annotations

from typing import Any

from .config import PLANS

LANGUAGES = {
    "en": "🇬🇧 English",
    "az": "🇦🇿 Azərbaycan",
    "ru": "🇷🇺 Русский",
}

BUTTONS: dict[str, dict[str, str]] = {
    "packages": {
        "en": "📦 Packages",
        "az": "📦 Paketlər",
        "ru": "📦 Пакеты",
    },
    "subscription": {
        "en": "👤 My Subscription",
        "az": "👤 Abunəliyim",
        "ru": "👤 Моя подписка",
    },
    "contact": {
        "en": "💬 Contact Us",
        "az": "💬 Bizə yaz",
        "ru": "💬 Написать нам",
    },
    "change_language": {
        "en": "🌐 Change Language",
        "az": "🌐 Dili dəyiş",
        "ru": "🌐 Сменить язык",
    },
    "admin_users": {
        "en": "👥 Users",
        "az": "👥 İstifadəçilər",
        "ru": "👥 Пользователи",
    },
    "admin_broadcast": {
        "en": "📢 Broadcast",
        "az": "📢 Hamıya mesaj",
        "ru": "📢 Рассылка",
    },
    "admin_messages": {
        "en": "💬 Messages",
        "az": "💬 Mesajlar",
        "ru": "💬 Сообщения",
    },
    "switch_user": {
        "en": "🧑 User Menu",
        "az": "🧑 İstifadəçi menyusu",
        "ru": "🧑 Меню пользователя",
    },
    "switch_admin": {
        "en": "🛠 Admin Menu",
        "az": "🛠 Admin menyusu",
        "ru": "🛠 Меню администратора",
    },
    "contact_admin": {
        "en": "💳 Contact Admin",
        "az": "💳 Adminlə əlaqə saxla",
        "ru": "💳 Связаться с админом",
    },
    "deactivate_package": {
        "en": "⛔ Deactivate Package",
        "az": "⛔ Paketi deaktiv et",
        "ru": "⛔ Деактивировать пакет",
    },
    "back_to_users": {
        "en": "⬅️ Back to Users",
        "az": "⬅️ İstifadəçilərə qayıt",
        "ru": "⬅️ Назад к пользователям",
    },
    "reply_item": {
        "en": "💬 Reply",
        "az": "💬 Cavabla",
        "ru": "💬 Ответить",
    },
    "delete_item": {
        "en": "🗑 Delete",
        "az": "🗑 Sil",
        "ru": "🗑 Удалить",
    },

    # Köhnə açarlar qalsın ki, bot.py dəyişənə qədər xəta verməsin
    "review": {
        "en": "💬 Contact Us",
        "az": "💬 Bizə yaz",
        "ru": "💬 Написать нам",
    },
    "support": {
        "en": "💬 Contact Us",
        "az": "💬 Bizə yaz",
        "ru": "💬 Написать нам",
    },
    "admin_reviews": {
        "en": "💬 Messages",
        "az": "💬 Mesajlar",
        "ru": "💬 Сообщения",
    },
    "admin_complaints": {
        "en": "💬 Messages",
        "az": "💬 Mesajlar",
        "ru": "💬 Сообщения",
    },
    "admin_upload": {
        "en": "📥 Update Excel",
        "az": "📥 Excel yenilə",
        "ru": "📥 Обновить Excel",
    },
    "admin_manage_packages": {
        "en": "🔐 Manage Packages",
        "az": "🔐 Paketləri idarə et",
        "ru": "🔐 Управление пакетами",
    },
}

TEXTS: dict[str, dict[str, str]] = {
    "choose_language": {
        "en": "Welcome to <b>{brand}</b>\nPlease choose your language.",
        "az": "<b>{brand}</b> botuna xoş gəldin\nZəhmət olmasa dil seç.",
        "ru": "Добро пожаловать в <b>{brand}</b>\nПожалуйста, выберите язык.",
    },
    "welcome": {
        "en": "<b>{brand}</b> delivers curated product links for eCommerce sellers. Choose an option below.",
        "az": "<b>{brand}</b> e-commerce satıcıları üçün seçilmiş məhsul linklərini planına uyğun göndərir. Aşağıdan seçim et.",
        "ru": "<b>{brand}</b> отправляет отобранные товарные ссылки для e-commerce продавцов. Выберите действие ниже.",
    },
    "packages_title": {
        "en": "Choose your monthly package:",
        "az": "Aylıq paketini seç:",
        "ru": "Выберите ежемесячный пакет:",
    },
    "subscription_none": {
        "en": "You do not have an active package yet. Open Packages to choose one.",
        "az": "Hələ aktiv paket yoxdur. Paketlər bölməsindən birini seç.",
        "ru": "У вас пока нет активного пакета. Откройте раздел Пакеты и выберите один.",
    },
    "subscription_active": {
        "en": "<b>Your subscription</b>\nPlan: <b>{plan}</b>\nPrice: <b>{price}</b>\nStarted: <b>{started}</b>\nExpires: <b>{expires}</b>\nNext delivery: <b>{next_delivery}</b>\nRemaining unseen products: <b>{remaining}</b>",
        "az": "<b>Sənin abunəliyin</b>\nPaket: <b>{plan}</b>\nQiymət: <b>{price}</b>\nBaşlama tarixi: <b>{started}</b>\nBitmə tarixi: <b>{expires}</b>\nNövbəti göndəriş: <b>{next_delivery}</b>\nGörmədiyin qalan məhsullar: <b>{remaining}</b>",
        "ru": "<b>Ваша подписка</b>\nТариф: <b>{plan}</b>\nЦена: <b>{price}</b>\nДата старта: <b>{started}</b>\nДата окончания: <b>{expires}</b>\nСледующая отправка: <b>{next_delivery}</b>\nОставшиеся неповторяющиеся товары: <b>{remaining}</b>",
    },
    "contact_prompt": {
        "en": "Write your message in one message.",
        "az": "Mesajını bir mesajda yaz.",
        "ru": "Напишите ваше сообщение одним сообщением.",
    },
    "message_sent": {
        "en": "Your message has been sent.",
        "az": "Mesajın göndərildi.",
        "ru": "Ваше сообщение отправлено.",
    },
    "broadcast_prompt": {
        "en": "Send the message you want to broadcast to all users.",
        "az": "Bütün istifadəçilərə göndərmək istədiyin mesajı yaz.",
        "ru": "Отправьте сообщение, которое нужно разослать всем пользователям.",
    },
    "broadcast_done": {
        "en": "Broadcast completed. Delivered: <b>{success}</b> | Failed: <b>{failed}</b>",
        "az": "Kütləvi mesajlaşma tamamlandı. Göndərildi: <b>{success}</b> | Uğursuz: <b>{failed}</b>",
        "ru": "Рассылка завершена. Доставлено: <b>{success}</b> | Ошибок: <b>{failed}</b>",
    },
    "upload_prompt": {
        "en": "Send the Excel or CSV file now. Required columns: <b>name</b> and <b>link</b>.",
        "az": "İndi Excel və ya CSV faylını göndər. Lazım olan sütunlar: <b>name</b> və <b>link</b>.",
        "ru": "Отправьте Excel или CSV файл. Обязательные колонки: <b>name</b> и <b>link</b>.",
    },
    "upload_success": {
        "en": "Product list updated successfully.\nCreated: <b>{created}</b>\nUpdated: <b>{updated}</b>\nDeactivated: <b>{deactivated}</b>\nActive products: <b>{active}</b>",
        "az": "Məhsul siyahısı uğurla yeniləndi.\nYeni: <b>{created}</b>\nYenilənən: <b>{updated}</b>\nDeaktiv edilən: <b>{deactivated}</b>\nAktiv məhsullar: <b>{active}</b>",
        "ru": "Список товаров успешно обновлён.\nСоздано: <b>{created}</b>\nОбновлено: <b>{updated}</b>\nДеактивировано: <b>{deactivated}</b>\nАктивных товаров: <b>{active}</b>",
    },
    "upload_error": {
        "en": "File could not be imported. Make sure the file has name and link columns.",
        "az": "Fayl import olunmadı. name və link sütunlarının olduğuna əmin ol.",
        "ru": "Файл не удалось импортировать. Убедитесь, что есть колонки name и link.",
    },
    "language_updated": {
        "en": "Language updated successfully.",
        "az": "Dil uğurla dəyişdirildi.",
        "ru": "Язык успешно обновлён.",
    },
    "list_empty": {
        "en": "No data yet.",
        "az": "Hələ məlumat yoxdur.",
        "ru": "Пока данных нет.",
    },
    "new_product": {
        "en": "📦 <b>New product delivered</b>\n\nName: <b>{name}</b>\nLink: {link}",
        "az": "📦 <b>Yeni məhsul göndərildi</b>\n\nAd: <b>{name}</b>\nLink: {link}",
        "ru": "📦 <b>Новый товар отправлен</b>\n\nНазвание: <b>{name}</b>\nСсылка: {link}",
    },
    "catalog_empty": {
        "en": "The product catalog is empty. Ask the admin to upload an Excel file.",
        "az": "Məhsul kataloqu boşdur. Adminin Excel faylı yükləməsi lazımdır.",
        "ru": "Каталог товаров пуст. Попросите администратора загрузить Excel файл.",
    },
    "no_more_products": {
        "en": "You have already received all currently active products. New products will arrive after the catalog is updated.",
        "az": "Hazırda aktiv olan bütün məhsulları artıq almısan. Kataloq yenilənəndə yeni məhsullar gələcək.",
        "ru": "Вы уже получили все активные товары. Новые товары появятся после обновления каталога.",
    },
    "unknown_message": {
        "en": "Choose one of the menu options below.",
        "az": "Aşağıdakı menyudan seçim et.",
        "ru": "Выберите один из пунктов меню ниже.",
    },
    "admin_only": {
        "en": "This section is for admins only.",
        "az": "Bu bölmə yalnız adminlər üçündür.",
        "ru": "Этот раздел только для администраторов.",
    },
    "plan_request": {
        "en": "Selected plan: <b>{plan}</b>\nPrice: <b>{price}</b>\n\nTo activate your package, contact admin and send your Telegram ID below.\n<b>Your Telegram ID:</b> <code>{telegram_id}</code>",
        "az": "Seçilən paket: <b>{plan}</b>\nQiymət: <b>{price}</b>\n\nPaketin aktivləşdirilməsi üçün adminlə əlaqə saxla və aşağıdakı Telegram ID-ni göndər.\n<b>Sənin Telegram ID-n:</b> <code>{telegram_id}</code>",
        "ru": "Выбранный тариф: <b>{plan}</b>\nЦена: <b>{price}</b>\n\nЧтобы активировать тариф, свяжитесь с админом и отправьте Telegram ID ниже.\n<b>Ваш Telegram ID:</b> <code>{telegram_id}</code>",
    },
    "package_request_sent": {
        "en": "Your request has been sent to admin. Please complete payment and share your Telegram ID.",
        "az": "Sorğun adminə göndərildi. Ödənişi et və Telegram ID-ni adminə göndər.",
        "ru": "Ваш запрос отправлен админу. Оплатите и отправьте админу свой Telegram ID.",
    },
    "manage_packages_prompt": {
        "en": "Send the user's Telegram ID.",
        "az": "İstifadəçinin Telegram ID-sini göndər.",
        "ru": "Отправьте Telegram ID пользователя.",
    },
    "manage_packages_not_found": {
        "en": "User not found.",
        "az": "İstifadəçi tapılmadı.",
        "ru": "Пользователь не найден.",
    },
    "manage_packages_choose": {
        "en": "Choose a package for user <code>{telegram_id}</code>.",
        "az": "<code>{telegram_id}</code> üçün paketi seç.",
        "ru": "Выберите тариф для пользователя <code>{telegram_id}</code>.",
    },
    "package_activated_admin": {
        "en": "Package activated for user <code>{telegram_id}</code>: <b>{plan}</b>",
        "az": "<code>{telegram_id}</code> üçün paket aktiv edildi: <b>{plan}</b>",
        "ru": "Для пользователя <code>{telegram_id}</code> активирован тариф: <b>{plan}</b>",
    },
    "package_deactivated_admin": {
        "en": "Package deactivated for user <code>{telegram_id}</code>.",
        "az": "<code>{telegram_id}</code> üçün paket deaktiv edildi.",
        "ru": "Пакет для пользователя <code>{telegram_id}</code> деактивирован.",
    },
    "package_activated_user": {
        "en": "Your package is now active: <b>{plan}</b>",
        "az": "Paketin artıq aktivdir: <b>{plan}</b>",
        "ru": "Ваш тариф теперь активен: <b>{plan}</b>",
    },
    "package_deactivated_user": {
        "en": "Your package has been deactivated.",
        "az": "Paketin deaktiv edildi.",
        "ru": "Ваш тариф был деактивирован.",
    },
    "package_expired_user": {
        "en": "Your plan has expired. Contact the admin to renew or change your plan.",
        "az": "Planınızın müddəti başa çatdı. Planı uzatmaq və ya dəyişmək üçün adminlə əlaqə saxlayın.",
        "ru": "Срок действия вашего тарифа истёк. Свяжитесь с администратором, чтобы продлить или изменить тариф.",
    },
    "package_expired_admin": {
        "en": "User <code>{telegram_id}</code> package expired and was deactivated automatically.",
        "az": "<code>{telegram_id}</code> istifadəçisinin paketi bitdi və avtomatik deaktiv edildi.",
        "ru": "Пакет пользователя <code>{telegram_id}</code> истёк и был автоматически деактивирован.",
    },
    "user_list_title": {
        "en": "<b>User list</b>\nPage: <b>{page}</b>/<b>{pages}</b>\nTotal users: <b>{total_users}</b> | Active subscriptions: <b>{active_subscriptions}</b>",
        "az": "<b>İstifadəçi siyahısı</b>\nSəhifə: <b>{page}</b>/<b>{pages}</b>\nÜmumi istifadəçi: <b>{total_users}</b> | Aktiv abunə: <b>{active_subscriptions}</b>",
        "ru": "<b>Список пользователей</b>\nСтраница: <b>{page}</b>/<b>{pages}</b>\nВсего пользователей: <b>{total_users}</b> | Активных подписок: <b>{active_subscriptions}</b>",
    },
    "user_card": {
        "en": "<b>User</b>\nName: {name}\nTelegram ID: <code>{telegram_id}</code>\nLanguage: <b>{language}</b>\nPackage: <b>{package}</b>\nStatus: <b>{status}</b>",
        "az": "<b>İstifadəçi</b>\nAd: {name}\nTelegram ID: <code>{telegram_id}</code>\nDil: <b>{language}</b>\nPaket: <b>{package}</b>\nStatus: <b>{status}</b>",
        "ru": "<b>Пользователь</b>\nИмя: {name}\nTelegram ID: <code>{telegram_id}</code>\nЯзык: <b>{language}</b>\nТариф: <b>{package}</b>\nСтатус: <b>{status}</b>",
    },
    "status_active": {
        "en": "Active",
        "az": "Aktiv",
        "ru": "Активен",
    },
    "status_inactive": {
        "en": "Inactive",
        "az": "Deaktiv",
        "ru": "Неактивен",
    },
    "admin_message_detail": {
        "en": "<b>Message</b>\nFrom: {name}\nTelegram ID: <code>{telegram_id}</code>\nDate: <b>{date}</b>\n\n{text}",
        "az": "<b>Mesaj</b>\nGöndərən: {name}\nTelegram ID: <code>{telegram_id}</code>\nTarix: <b>{date}</b>\n\n{text}",
        "ru": "<b>Сообщение</b>\nОт: {name}\nTelegram ID: <code>{telegram_id}</code>\nДата: <b>{date}</b>\n\n{text}",
    },
    "reply_prompt_message": {
        "en": "Send your reply in one message.",
        "az": "Cavabı bir mesajda yaz.",
        "ru": "Отправьте ответ одним сообщением.",
    },
    "reply_sent": {
        "en": "Reply sent.",
        "az": "Cavab göndərildi.",
        "ru": "Ответ отправлен.",
    },
    "message_deleted": {
        "en": "Message deleted.",
        "az": "Mesaj silindi.",
        "ru": "Сообщение удалено.",
    },
    "item_not_found": {
        "en": "Item not found.",
        "az": "Məlumat tapılmadı.",
        "ru": "Элемент не найден.",
    },
    "message_reply_user": {
        "en": "💬 <b>Admin reply</b>\n\n{text}",
        "az": "💬 <b>Admin cavabı</b>\n\n{text}",
        "ru": "💬 <b>Ответ администратора</b>\n\n{text}",
    },

    # Köhnə açarlar qalsın ki, bot.py dəyişənə qədər xəta verməsin
    "review_prompt": {
        "en": "Write your message in one message.",
        "az": "Mesajını bir mesajda yaz.",
        "ru": "Напишите ваше сообщение одним сообщением.",
    },
    "review_saved": {
        "en": "Your message has been sent.",
        "az": "Mesajın göndərildi.",
        "ru": "Ваше сообщение отправлено.",
    },
    "support_prompt": {
        "en": "Write your message in one message.",
        "az": "Mesajını bir mesajda yaz.",
        "ru": "Напишите ваше сообщение одним сообщением.",
    },
    "support_saved": {
        "en": "Your message has been sent.",
        "az": "Mesajın göndərildi.",
        "ru": "Ваше сообщение отправлено.",
    },
    "review_detail": {
        "en": "<b>Message</b>\nFrom: {name}\nTelegram ID: <code>{telegram_id}</code>\nDate: <b>{date}</b>\n\n{text}",
        "az": "<b>Mesaj</b>\nGöndərən: {name}\nTelegram ID: <code>{telegram_id}</code>\nTarix: <b>{date}</b>\n\n{text}",
        "ru": "<b>Сообщение</b>\nОт: {name}\nTelegram ID: <code>{telegram_id}</code>\nДата: <b>{date}</b>\n\n{text}",
    },
    "complaint_detail": {
        "en": "<b>Message</b>\nFrom: {name}\nTelegram ID: <code>{telegram_id}</code>\nDate: <b>{date}</b>\n\n{text}",
        "az": "<b>Mesaj</b>\nGöndərən: {name}\nTelegram ID: <code>{telegram_id}</code>\nTarix: <b>{date}</b>\n\n{text}",
        "ru": "<b>Сообщение</b>\nОт: {name}\nTelegram ID: <code>{telegram_id}</code>\nДата: <b>{date}</b>\n\n{text}",
    },
    "reply_prompt_review": {
        "en": "Send your reply in one message.",
        "az": "Cavabı bir mesajda yaz.",
        "ru": "Отправьте ответ одним сообщением.",
    },
    "reply_prompt_complaint": {
        "en": "Send your reply in one message.",
        "az": "Cavabı bir mesajda yaz.",
        "ru": "Отправьте ответ одним сообщением.",
    },
    "review_deleted": {
        "en": "Message deleted.",
        "az": "Mesaj silindi.",
        "ru": "Сообщение удалено.",
    },
    "complaint_deleted": {
        "en": "Message deleted.",
        "az": "Mesaj silindi.",
        "ru": "Сообщение удалено.",
    },
    "review_reply_user": {
        "en": "💬 <b>Admin reply</b>\n\n{text}",
        "az": "💬 <b>Admin cavabı</b>\n\n{text}",
        "ru": "💬 <b>Ответ администратора</b>\n\n{text}",
    },
    "complaint_reply_user": {
        "en": "💬 <b>Admin reply</b>\n\n{text}",
        "az": "💬 <b>Admin cavabı</b>\n\n{text}",
        "ru": "💬 <b>Ответ администратора</b>\n\n{text}",
    },
}

PLAN_LABELS: dict[str, dict[str, str]] = {
    "every_3_days": {
        "en": "1 product every 3 days",
        "az": "Hər 3 gündən 1 məhsul",
        "ru": "1 товар каждые 3 дня",
    },
    "every_2_days": {
        "en": "1 product every 2 days",
        "az": "Hər 2 gündən 1 məhsul",
        "ru": "1 товар каждые 2 дня",
    },
    "daily": {
        "en": "1 product every day",
        "az": "Hər gün 1 məhsul",
        "ru": "1 товар каждый день",
    },
}


def tr(lang: str, key: str, **kwargs: Any) -> str:
    lang = lang if lang in LANGUAGES else "en"
    template = TEXTS.get(key, {}).get(lang) or TEXTS.get(key, {}).get("en") or key
    return template.format(**kwargs)


def button(lang: str, key: str) -> str:
    lang = lang if lang in LANGUAGES else "en"
    return BUTTONS[key].get(lang, BUTTONS[key]["en"])


def resolve_action(text: str) -> str | None:
    for action, mapping in BUTTONS.items():
        if text in mapping.values():
            return action
    return None


def plan_label(lang: str, plan_code: str) -> str:
    lang = lang if lang in LANGUAGES else "en"
    mapping = PLAN_LABELS.get(plan_code)
    if mapping is None:
        return plan_code
    return mapping.get(lang, mapping["en"])


def plan_price(lang: str, plan_code: str) -> str:
    lang = lang if lang in LANGUAGES else "en"
    prices = PLANS[plan_code]["prices"]
    assert isinstance(prices, dict)
    return str(prices.get(lang, prices["en"]))