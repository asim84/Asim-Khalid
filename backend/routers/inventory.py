from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import InventoryItem, get_db

router = APIRouter(prefix="/api/inventory", tags=["inventory"])


class InventoryStatus(BaseModel):
    id: int
    sku: str
    asin: str | None
    title: str
    quantity_available: int
    quantity_inbound: int
    quantity_reserved: int
    reorder_point: int
    days_of_cover: float
    sell_price_pence: int
    cost_price_pence: int
    status: str
    last_updated: str


def _status(item: InventoryItem) -> str:
    if item.quantity_available <= 0 or item.days_of_cover < 7:
        return "critical"
    if item.days_of_cover < 14 or item.quantity_available <= item.reorder_point:
        return "warning"
    return "ok"


def _to_response(item: InventoryItem) -> InventoryStatus:
    return InventoryStatus(
        id=item.id,
        sku=item.sku,
        asin=item.asin,
        title=item.title,
        quantity_available=item.quantity_available,
        quantity_inbound=item.quantity_inbound,
        quantity_reserved=item.quantity_reserved,
        reorder_point=item.reorder_point,
        days_of_cover=round(item.days_of_cover, 1),
        sell_price_pence=item.sell_price_pence,
        cost_price_pence=item.cost_price_pence,
        status=_status(item),
        last_updated=item.last_updated.isoformat(),
    )


@router.get("/", response_model=list[InventoryStatus])
def get_inventory(db: Session = Depends(get_db)):
    items = db.query(InventoryItem).order_by(InventoryItem.days_of_cover.asc()).all()
    return [_to_response(i) for i in items]


@router.get("/alerts", response_model=list[InventoryStatus])
def get_inventory_alerts(db: Session = Depends(get_db)):
    items = db.query(InventoryItem).all()
    alerts = [i for i in items if _status(i) in ("critical", "warning")]
    alerts.sort(key=lambda i: i.days_of_cover)
    return [_to_response(i) for i in alerts]
