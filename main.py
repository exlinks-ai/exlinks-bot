from __future__ import annotations

import logging
import sys
from pathlib import Path

from exlinks_bot.bot import ExLinksBot
from exlinks_bot.config import settings
from exlinks_bot.db import Database
from exlinks_bot.services import parse_product_file


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


def import_products_from_data(database: Database) -> None:
    logger = logging.getLogger(__name__)
    data_dir = Path("data")

    candidates = [
        data_dir / "sample_products.xlsx",
        data_dir / "sample_products.xlsm",
        data_dir / "sample_products.csv",
    ]

    file_path = next((path for path in candidates if path.exists()), None)
    if file_path is None:
        logger.info("No product file found in data folder. Skipping import.")
        return

    try:
        records = parse_product_file(file_path)
        stats = database.import_products(records)
        logger.info(
            "Products imported from %s | created=%s updated=%s deactivated=%s active=%s",
            file_path.name,
            stats.created,
            stats.updated,
            stats.deactivated,
            stats.active,
        )
    except Exception as exc:
        logger.exception("Failed to import products from %s: %s", file_path, exc)


def main() -> None:
    configure_logging()

    if not settings.bot_token:
        print("BOT_TOKEN is missing. Please create a .env file or set environment variables.")
        sys.exit(1)

    database = Database(settings.database_url)
    database.init_db()
    import_products_from_data(database)

    bot = ExLinksBot(settings=settings, db=database)
    application = bot.build_application()
    application.run_polling(drop_pending_updates=False)


if __name__ == "__main__":
    main()