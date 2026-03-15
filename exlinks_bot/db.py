from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Iterator

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    create_engine,
    func,
    select,
    update,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship, sessionmaker


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    username: Mapped[str | None] = mapped_column(String(255), nullable=True)
    first_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    language_code: Mapped[str] = mapped_column(String(10), default="en")
    package_code: Mapped[str | None] = mapped_column(String(50), nullable=True)
    package_active: Mapped[bool] = mapped_column(Boolean, default=False)
    package_started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    next_delivery_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    package_expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    deliveries: Mapped[list["Delivery"]] = relationship(back_populates="user")


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(500))
    link: Mapped[str] = mapped_column(Text, unique=True, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    deliveries: Mapped[list["Delivery"]] = relationship(back_populates="product")


class Delivery(Base):
    __tablename__ = "deliveries"
    __table_args__ = (UniqueConstraint("user_id", "product_id", name="uq_user_product_delivery"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)
    sent_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user: Mapped["User"] = relationship(back_populates="deliveries")
    product: Mapped["Product"] = relationship(back_populates="deliveries")


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    text: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class Complaint(Base):
    __tablename__ = "complaints"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    text: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(50), default="open")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


@dataclass
class ImportStats:
    created: int
    updated: int
    deactivated: int
    active: int


class Database:
    def __init__(self, database_url: str):
        connect_args = {"check_same_thread": False} if database_url.startswith("sqlite") else {}
        self.engine = create_engine(database_url, future=True, pool_pre_ping=True, connect_args=connect_args)
        self.SessionLocal = sessionmaker(bind=self.engine, autoflush=False, autocommit=False, expire_on_commit=False)

    def init_db(self) -> None:
        Base.metadata.create_all(self.engine)

    @contextmanager
    def session(self) -> Iterator[Session]:
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def upsert_user(self, telegram_id: int, username: str | None, first_name: str | None) -> User:
        with self.session() as session:
            user = session.scalar(select(User).where(User.telegram_id == telegram_id))
            if user is None:
                user = User(
                    telegram_id=telegram_id,
                    username=username,
                    first_name=first_name,
                )
                session.add(user)
                session.flush()
            else:
                user.username = username
                user.first_name = first_name
                user.updated_at = datetime.now(timezone.utc)
                session.add(user)
            session.flush()
            return user

    def get_user(self, telegram_id: int) -> User | None:
        with self.session() as session:
            return session.scalar(select(User).where(User.telegram_id == telegram_id))

    def get_user_by_telegram_id(self, telegram_id: int) -> User | None:
        with self.session() as session:
            return session.scalar(select(User).where(User.telegram_id == telegram_id))

    def set_language(self, telegram_id: int, language_code: str) -> None:
        with self.session() as session:
            user = session.scalar(select(User).where(User.telegram_id == telegram_id))
            if user is None:
                return
            user.language_code = language_code
            user.updated_at = datetime.now(timezone.utc)

    def set_package(
        self,
        telegram_id: int,
        package_code: str,
        next_delivery_at: datetime,
        package_expires_at: datetime,
    ) -> User | None:
        with self.session() as session:
            user = session.scalar(select(User).where(User.telegram_id == telegram_id))
            if user is None:
                return None

            now = datetime.now(timezone.utc)
            user.package_started_at = now
            user.package_code = package_code
            user.package_active = True
            user.next_delivery_at = next_delivery_at
            user.package_expires_at = package_expires_at
            user.updated_at = now
            session.flush()
            return user

    def deactivate_package(self, telegram_id: int) -> User | None:
        with self.session() as session:
            user = session.scalar(select(User).where(User.telegram_id == telegram_id))
            if user is None:
                return None

            user.package_active = False
            user.package_code = None
            user.package_started_at = None
            user.next_delivery_at = None
            user.package_expires_at = None
            user.updated_at = datetime.now(timezone.utc)
            session.flush()
            return user

    def update_next_delivery(self, user_id: int, next_delivery_at: datetime) -> None:
        with self.session() as session:
            user = session.get(User, user_id)
            if user is None:
                return
            user.next_delivery_at = next_delivery_at
            user.updated_at = datetime.now(timezone.utc)

    def get_due_users(self, now: datetime) -> list[User]:
        with self.session() as session:
            stmt = select(User).where(
                User.package_active.is_(True),
                User.package_code.is_not(None),
                User.next_delivery_at.is_not(None),
                User.next_delivery_at <= now,
            )
            return list(session.scalars(stmt).all())

    def get_expired_users(self, now: datetime) -> list[User]:
        with self.session() as session:
            stmt = select(User).where(
                User.package_active.is_(True),
                User.package_code.is_not(None),
                User.package_expires_at.is_not(None),
                User.package_expires_at <= now,
            )
            return list(session.scalars(stmt).all())

    def get_random_unsent_product(self, user_id: int) -> Product | None:
        with self.session() as session:
            delivered_subquery = select(Delivery.product_id).where(Delivery.user_id == user_id)
            stmt = (
                select(Product)
                .where(Product.is_active.is_(True), Product.id.not_in(delivered_subquery))
                .order_by(func.random())
                .limit(1)
            )
            return session.scalar(stmt)

    def add_delivery(self, user_id: int, product_id: int, sent_at: datetime | None = None) -> None:
        with self.session() as session:
            session.add(
                Delivery(
                    user_id=user_id,
                    product_id=product_id,
                    sent_at=sent_at or datetime.now(timezone.utc),
                )
            )

    def add_review(self, telegram_id: int, text: str) -> None:
        with self.session() as session:
            user = session.scalar(select(User).where(User.telegram_id == telegram_id))
            session.add(Review(user_id=user.id if user else None, text=text))

    def add_complaint(self, telegram_id: int, text: str) -> None:
        with self.session() as session:
            user = session.scalar(select(User).where(User.telegram_id == telegram_id))
            session.add(Complaint(user_id=user.id if user else None, text=text))

    def import_products(self, records: list[dict[str, str]]) -> ImportStats:
        cleaned: list[dict[str, str]] = []
        seen_links: set[str] = set()

        for item in records:
            name = item.get("name", "").strip()
            link = item.get("link", "").strip()
            if not name or not link or link in seen_links:
                continue
            cleaned.append({"name": name, "link": link})
            seen_links.add(link)

        if not cleaned:
            raise ValueError("No valid products found in the uploaded file.")

        now = datetime.now(timezone.utc)
        created = 0
        updated = 0

        with self.session() as session:
            links = [item["link"] for item in cleaned]
            existing = {
                product.link: product
                for product in session.scalars(select(Product).where(Product.link.in_(links))).all()
            }

            for item in cleaned:
                product = existing.get(item["link"])
                if product is None:
                    session.add(
                        Product(
                            name=item["name"],
                            link=item["link"],
                            is_active=True,
                            created_at=now,
                            updated_at=now,
                        )
                    )
                    created += 1
                else:
                    changed = False
                    if product.name != item["name"]:
                        product.name = item["name"]
                        changed = True
                    if not product.is_active:
                        product.is_active = True
                        changed = True
                    product.updated_at = now
                    if changed:
                        updated += 1

            session.flush()

            deactivate_stmt = (
                update(Product)
                .where(Product.link.not_in(links), Product.is_active.is_(True))
                .values(is_active=False, updated_at=now)
            )
            result = session.execute(deactivate_stmt)
            session.flush()

            deactivated = int(result.rowcount or 0)
            active_count = session.scalar(select(func.count()).select_from(Product).where(Product.is_active.is_(True))) or 0

        return ImportStats(
            created=created,
            updated=updated,
            deactivated=deactivated,
            active=int(active_count),
        )

    def get_stats(self) -> dict[str, int]:
        with self.session() as session:
            total_users = session.scalar(select(func.count()).select_from(User)) or 0
            active_subscriptions = session.scalar(
                select(func.count()).select_from(User).where(User.package_active.is_(True))
            ) or 0
            active_products = session.scalar(
                select(func.count()).select_from(Product).where(Product.is_active.is_(True))
            ) or 0
            reviews = session.scalar(select(func.count()).select_from(Review)) or 0
            complaints = session.scalar(select(func.count()).select_from(Complaint)) or 0

            return {
                "total_users": int(total_users),
                "active_subscriptions": int(active_subscriptions),
                "active_products": int(active_products),
                "reviews": int(reviews),
                "complaints": int(complaints),
            }

    def latest_users(self, limit: int = 10) -> list[User]:
        with self.session() as session:
            stmt = select(User).order_by(User.created_at.desc()).limit(limit)
            return list(session.scalars(stmt).all())

    def get_users_paginated(self, page: int = 1, per_page: int = 10) -> tuple[list[User], int]:
        if page < 1:
            page = 1
        if per_page < 1:
            per_page = 10

        with self.session() as session:
            total = int(session.scalar(select(func.count()).select_from(User)) or 0)
            stmt = (
                select(User)
                .order_by(User.created_at.desc())
                .offset((page - 1) * per_page)
                .limit(per_page)
            )
            users = list(session.scalars(stmt).all())
            return users, total

    def latest_reviews(self, limit: int = 10) -> list[tuple[Review, User | None]]:
        with self.session() as session:
            stmt = (
                select(Review, User)
                .join(User, Review.user_id == User.id, isouter=True)
                .order_by(Review.created_at.desc())
                .limit(limit)
            )
            return list(session.execute(stmt).all())

    def get_review(self, review_id: int) -> tuple[Review | None, User | None]:
        with self.session() as session:
            row = session.execute(
                select(Review, User)
                .join(User, Review.user_id == User.id, isouter=True)
                .where(Review.id == review_id)
            ).first()
            if row is None:
                return None, None
            return row[0], row[1]

    def delete_review(self, review_id: int) -> bool:
        with self.session() as session:
            review = session.get(Review, review_id)
            if review is None:
                return False
            session.delete(review)
            return True

    def latest_complaints(self, limit: int = 10) -> list[tuple[Complaint, User | None]]:
        with self.session() as session:
            stmt = (
                select(Complaint, User)
                .join(User, Complaint.user_id == User.id, isouter=True)
                .order_by(Complaint.created_at.desc())
                .limit(limit)
            )
            return list(session.execute(stmt).all())

    def get_complaint(self, complaint_id: int) -> tuple[Complaint | None, User | None]:
        with self.session() as session:
            row = session.execute(
                select(Complaint, User)
                .join(User, Complaint.user_id == User.id, isouter=True)
                .where(Complaint.id == complaint_id)
            ).first()
            if row is None:
                return None, None
            return row[0], row[1]

    def set_complaint_status(self, complaint_id: int, status: str) -> bool:
        with self.session() as session:
            complaint = session.get(Complaint, complaint_id)
            if complaint is None:
                return False
            complaint.status = status
            return True

    def delete_complaint(self, complaint_id: int) -> bool:
        with self.session() as session:
            complaint = session.get(Complaint, complaint_id)
            if complaint is None:
                return False
            session.delete(complaint)
            return True

    def latest_all_messages(self, limit: int = 20):
        with self.session() as session:
            reviews = session.execute(
                select(Review, User)
                .join(User, Review.user_id == User.id, isouter=True)
                .order_by(Review.created_at.desc())
                .limit(limit)
            ).all()

            complaints = session.execute(
                select(Complaint, User)
                .join(User, Complaint.user_id == User.id, isouter=True)
                .order_by(Complaint.created_at.desc())
                .limit(limit)
            ).all()

            items = []

            for review, user in reviews:
                items.append(
                    {
                        "kind": "review",
                        "id": review.id,
                        "text": review.text,
                        "created_at": review.created_at,
                        "user": user,
                    }
                )

            for complaint, user in complaints:
                items.append(
                    {
                        "kind": "complaint",
                        "id": complaint.id,
                        "text": complaint.text,
                        "created_at": complaint.created_at,
                        "user": user,
                    }
                )

            items.sort(key=lambda x: x["created_at"], reverse=True)
            return items[:limit]

    def get_message_item(self, kind: str, item_id: int):
        with self.session() as session:
            if kind == "review":
                row = session.execute(
                    select(Review, User)
                    .join(User, Review.user_id == User.id, isouter=True)
                    .where(Review.id == item_id)
                ).first()
            elif kind == "complaint":
                row = session.execute(
                    select(Complaint, User)
                    .join(User, Complaint.user_id == User.id, isouter=True)
                    .where(Complaint.id == item_id)
                ).first()
            else:
                return None, None

            if row is None:
                return None, None
            return row[0], row[1]

    def delete_message_item(self, kind: str, item_id: int) -> bool:
        with self.session() as session:
            if kind == "review":
                item = session.get(Review, item_id)
            elif kind == "complaint":
                item = session.get(Complaint, item_id)
            else:
                return False

            if item is None:
                return False

            session.delete(item)
            return True

    def count_remaining_products(self, user_id: int) -> int:
        with self.session() as session:
            delivered_subquery = select(Delivery.product_id).where(Delivery.user_id == user_id)
            stmt = select(func.count()).select_from(Product).where(
                Product.is_active.is_(True),
                Product.id.not_in(delivered_subquery),
            )
            return int(session.scalar(stmt) or 0)

    def get_all_user_chat_ids(self) -> list[int]:
        with self.session() as session:
            return [int(value) for value in session.scalars(select(User.telegram_id)).all()]
