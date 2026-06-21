from datetime import datetime, timedelta

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import FeeRecord, Order, get_db

router = APIRouter(prefix="/api/fees", tags=["fees"])


class FeeSummary(BaseModel):
    total_fees_pence: int
    referral_fees_pence: int
    fba_fees_pence: int
    other_fees_pence: int
    fee_percentage: float
    period_days: int


class FeeTypeBreakdown(BaseModel):
    fee_type: str
    total_pence: int
    percentage: float


def _period_days(period: str) -> int:
    return {"30d": 30, "90d": 90}.get(period, 30)


@router.get("/summary", response_model=FeeSummary)
def get_fee_summary(period: str = "30d", db: Session = Depends(get_db)):
    days = _period_days(period)
    start = datetime.utcnow() - timedelta(days=days)

    fees = db.query(FeeRecord).filter(FeeRecord.recorded_at >= start).all()
    orders = db.query(Order).filter(Order.order_date >= start).all()

    total_revenue = sum(o.revenue_pence for o in orders)
    total_fees = sum(f.amount_pence for f in fees)

    referral = sum(f.amount_pence for f in fees if "referral" in f.fee_type.lower())
    fba = sum(f.amount_pence for f in fees if "fba" in f.fee_type.lower() or "fulfillment" in f.fee_type.lower())
    other = total_fees - referral - fba

    fee_pct = (total_fees / total_revenue * 100) if total_revenue else 0.0

    return FeeSummary(
        total_fees_pence=total_fees,
        referral_fees_pence=referral,
        fba_fees_pence=fba,
        other_fees_pence=other,
        fee_percentage=round(fee_pct, 1),
        period_days=days,
    )


@router.get("/breakdown", response_model=list[FeeTypeBreakdown])
def get_fee_breakdown(period: str = "30d", db: Session = Depends(get_db)):
    days = _period_days(period)
    start = datetime.utcnow() - timedelta(days=days)

    fees = db.query(FeeRecord).filter(FeeRecord.recorded_at >= start).all()
    total = sum(f.amount_pence for f in fees) or 1

    agg: dict[str, int] = {}
    for f in fees:
        agg[f.fee_type] = agg.get(f.fee_type, 0) + f.amount_pence

    return [
        FeeTypeBreakdown(
            fee_type=ft,
            total_pence=amt,
            percentage=round(amt / total * 100, 1),
        )
        for ft, amt in sorted(agg.items(), key=lambda x: x[1], reverse=True)
    ]
