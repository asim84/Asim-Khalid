from datetime import datetime, timedelta

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Session

from database import Order, get_db

router = APIRouter(prefix="/api/sales", tags=["sales"])


class SalesSummary(BaseModel):
    total_revenue_pence: int
    total_orders: int
    total_units: int
    avg_order_value_pence: int
    revenue_change_pct: float
    orders_change_pct: float
    period_days: int


class DailyStat(BaseModel):
    date: str
    revenue_pence: int
    orders: int
    units: int


class SKUSale(BaseModel):
    sku: str
    title: str
    revenue_pence: int
    units: int
    rank: int


def _period_days(period: str) -> int:
    mapping = {"7d": 7, "30d": 30, "90d": 90}
    return mapping.get(period, 30)


@router.get("/summary", response_model=SalesSummary)
def get_sales_summary(period: str = "30d", db: Session = Depends(get_db)):
    days = _period_days(period)
    now = datetime.utcnow()
    start = now - timedelta(days=days)
    prev_start = start - timedelta(days=days)

    def query_period(from_dt: datetime, to_dt: datetime):
        rows = db.query(Order).filter(Order.order_date >= from_dt, Order.order_date < to_dt).all()
        revenue = sum(o.revenue_pence for o in rows)
        orders = len(rows)
        units = sum(o.quantity for o in rows)
        return revenue, orders, units

    rev, ord_, units = query_period(start, now)
    prev_rev, prev_ord, _ = query_period(prev_start, start)

    rev_change = ((rev - prev_rev) / prev_rev * 100) if prev_rev else 0.0
    ord_change = ((ord_ - prev_ord) / prev_ord * 100) if prev_ord else 0.0
    avg_ov = rev // ord_ if ord_ else 0

    return SalesSummary(
        total_revenue_pence=rev,
        total_orders=ord_,
        total_units=units,
        avg_order_value_pence=avg_ov,
        revenue_change_pct=round(rev_change, 1),
        orders_change_pct=round(ord_change, 1),
        period_days=days,
    )


@router.get("/chart", response_model=list[DailyStat])
def get_sales_chart(period: str = "30d", db: Session = Depends(get_db)):
    days = _period_days(period)
    start = datetime.utcnow() - timedelta(days=days)
    orders = db.query(Order).filter(Order.order_date >= start).all()

    daily: dict[str, dict] = {}
    for o in orders:
        day = o.order_date.strftime("%Y-%m-%d")
        if day not in daily:
            daily[day] = {"revenue_pence": 0, "orders": 0, "units": 0}
        daily[day]["revenue_pence"] += o.revenue_pence
        daily[day]["orders"] += 1
        daily[day]["units"] += o.quantity

    return [
        DailyStat(date=d, **v)
        for d, v in sorted(daily.items())
    ]


@router.get("/by_sku", response_model=list[SKUSale])
def get_sales_by_sku(period: str = "30d", db: Session = Depends(get_db)):
    days = _period_days(period)
    start = datetime.utcnow() - timedelta(days=days)
    orders = db.query(Order).filter(Order.order_date >= start).all()

    agg: dict[str, dict] = {}
    for o in orders:
        if o.sku not in agg:
            agg[o.sku] = {"title": o.title, "revenue_pence": 0, "units": 0}
        agg[o.sku]["revenue_pence"] += o.revenue_pence
        agg[o.sku]["units"] += o.quantity

    sorted_skus = sorted(agg.items(), key=lambda x: x[1]["revenue_pence"], reverse=True)
    return [
        SKUSale(sku=sku, rank=i + 1, **data)
        for i, (sku, data) in enumerate(sorted_skus)
    ]
