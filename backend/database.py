from datetime import datetime
from typing import Generator

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    Integer,
    String,
    create_engine,
)
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./bizai.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, nullable=False)  # "amazon" or "linnworks"
    marketplace = Column(String, nullable=False, default="UK")
    order_id = Column(String, unique=True, nullable=False, index=True)
    sku = Column(String, nullable=False, index=True)
    asin = Column(String, nullable=True)
    title = Column(String, nullable=False, default="")
    quantity = Column(Integer, nullable=False, default=1)
    revenue_pence = Column(Integer, nullable=False, default=0)
    currency = Column(String, nullable=False, default="GBP")
    fees_pence = Column(Integer, nullable=False, default=0)
    net_profit_pence = Column(Integer, nullable=False, default=0)
    order_date = Column(DateTime, nullable=False)
    status = Column(String, nullable=False, default="Shipped")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


class InventoryItem(Base):
    __tablename__ = "inventory_items"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String, unique=True, nullable=False, index=True)
    asin = Column(String, nullable=True)
    title = Column(String, nullable=False, default="")
    quantity_available = Column(Integer, nullable=False, default=0)
    quantity_inbound = Column(Integer, nullable=False, default=0)
    quantity_reserved = Column(Integer, nullable=False, default=0)
    reorder_point = Column(Integer, nullable=False, default=10)
    cost_price_pence = Column(Integer, nullable=False, default=0)
    sell_price_pence = Column(Integer, nullable=False, default=0)
    days_of_cover = Column(Float, nullable=False, default=0.0)
    last_updated = Column(DateTime, nullable=False, default=datetime.utcnow)


class FeeRecord(Base):
    __tablename__ = "fee_records"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String, nullable=False, index=True)
    fee_type = Column(String, nullable=False)
    amount_pence = Column(Integer, nullable=False, default=0)
    currency = Column(String, nullable=False, default="GBP")
    recorded_at = Column(DateTime, nullable=False, default=datetime.utcnow)


class AIInsight(Base):
    __tablename__ = "ai_insights"

    id = Column(Integer, primary_key=True, index=True)
    insight_type = Column(String, nullable=False)
    severity = Column(String, nullable=False, default="info")  # info/warning/critical
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    affected_skus = Column(String, nullable=True)  # comma-separated
    generated_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    is_read = Column(Boolean, nullable=False, default=False)


class SyncLog(Base):
    __tablename__ = "sync_logs"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, nullable=False)
    status = Column(String, nullable=False, default="success")  # success/error
    records_processed = Column(Integer, nullable=False, default=0)
    error_message = Column(String, nullable=True)
    synced_at = Column(DateTime, nullable=False, default=datetime.utcnow)


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
