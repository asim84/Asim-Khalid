import logging
import os
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.orm import Session

from analysis.ai_analyzer import AIAnalyzer
from connectors.amazon_connector import AmazonConnector
from connectors.dropbox_connector import DropboxConnector
from database import FeeRecord, InventoryItem, Order, SessionLocal, SyncLog
from parsers.linnworks_parser import detect_export_type, parse_inventory_csv, parse_orders_csv

logger = logging.getLogger(__name__)
scheduler = AsyncIOScheduler()


def _log(db: Session, source: str, status: str, records: int = 0, error: str | None = None):
    db.add(SyncLog(source=source, status=status, records_processed=records, error_message=error, synced_at=datetime.utcnow()))
    db.commit()


async def _sync_dropbox(db: Session):
    try:
        connector = DropboxConnector()
    except ValueError:
        logger.warning("Dropbox not configured, skipping")
        return

    processed_names = [r[0] for r in db.query(SyncLog.source).filter(SyncLog.source.like("dropbox:%"), SyncLog.status == "success").all()]
    processed_names = [n.replace("dropbox:", "") for n in processed_names]

    new_files = connector.list_new_files(processed_names)
    total = 0

    for f in new_files:
        try:
            content = connector.download_file(f["path"])
            export_type = detect_export_type(f["name"])

            if export_type == "orders":
                records = parse_orders_csv(content)
                for r in records:
                    if not r.get("order_id") or not r.get("sku"):
                        continue
                    exists = db.query(Order).filter(Order.order_id == r["order_id"]).first()
                    if not exists:
                        order_date = r.get("order_date") or datetime.utcnow()
                        if isinstance(order_date, str):
                            try:
                                from dateutil import parser as dp
                                order_date = dp.parse(order_date)
                            except Exception:
                                order_date = datetime.utcnow()
                        db.add(Order(
                            source=r.get("source", "linnworks"),
                            marketplace=r.get("marketplace", "UK"),
                            order_id=r["order_id"],
                            sku=r["sku"],
                            title=r.get("title", ""),
                            quantity=r.get("quantity", 1),
                            revenue_pence=r.get("revenue_pence", 0),
                            fees_pence=0,
                            net_profit_pence=r.get("revenue_pence", 0),
                            order_date=order_date,
                            status=r.get("status", "Shipped"),
                        ))
                        total += 1
                db.commit()

            elif export_type == "inventory":
                records = parse_inventory_csv(content)
                for r in records:
                    if not r.get("sku"):
                        continue
                    item = db.query(InventoryItem).filter(InventoryItem.sku == r["sku"]).first()
                    qty = r.get("stock_level", r.get("quantity_available", 0))
                    sell = r.get("sell_price_pence", r.get("retail_price_pence", 0))
                    cost = r.get("cost_price_pence", r.get("purchase_price_pence", 0))
                    reorder = r.get("minimum_level", r.get("reorder_point", 10))

                    daily_sales = _calc_daily_sales(db, r["sku"])
                    doc = (qty / daily_sales) if daily_sales > 0 else 999.0

                    if item:
                        item.quantity_available = qty
                        item.sell_price_pence = sell
                        item.cost_price_pence = cost
                        item.reorder_point = reorder
                        item.days_of_cover = doc
                        item.last_updated = datetime.utcnow()
                    else:
                        db.add(InventoryItem(
                            sku=r["sku"],
                            title=r.get("title", ""),
                            quantity_available=qty,
                            reorder_point=reorder,
                            cost_price_pence=cost,
                            sell_price_pence=sell,
                            days_of_cover=doc,
                            last_updated=datetime.utcnow(),
                        ))
                    total += 1
                db.commit()

            _log(db, f"dropbox:{f['name']}", "success", total)
        except Exception as e:
            logger.error("Error processing Dropbox file %s: %s", f["name"], e)
            _log(db, f"dropbox:{f['name']}", "error", 0, str(e))


def _calc_daily_sales(db: Session, sku: str) -> float:
    from datetime import timedelta
    from sqlalchemy import func
    result = db.query(func.sum(Order.quantity)).filter(
        Order.sku == sku,
        Order.order_date >= datetime.utcnow() - timedelta(days=30),
    ).scalar()
    return (result or 0) / 30.0


async def _sync_amazon(db: Session):
    connector = AmazonConnector()
    if not connector.refresh_token:
        logger.warning("Amazon SP-API not configured, skipping")
        return

    try:
        orders = await connector.get_orders(days_back=7)
        total = 0
        for o in orders:
            order_id = o.get("AmazonOrderId", "")
            if not order_id:
                continue
            exists = db.query(Order).filter(Order.order_id == order_id).first()
            if not exists:
                from dateutil import parser as dp
                order_date = dp.parse(o.get("PurchaseDate", "")) if o.get("PurchaseDate") else datetime.utcnow()
                revenue_pence = int(float(o.get("OrderTotal", {}).get("Amount", 0)) * 100)
                db.add(Order(
                    source="amazon",
                    marketplace=o.get("MarketplaceId", "UK"),
                    order_id=order_id,
                    sku="AMAZON-ORDER",
                    title="",
                    quantity=int(o.get("NumberOfItemsShipped", 1)),
                    revenue_pence=revenue_pence,
                    fees_pence=0,
                    net_profit_pence=revenue_pence,
                    order_date=order_date,
                    status=o.get("OrderStatus", "Shipped"),
                ))
                total += 1
        db.commit()
        _log(db, "amazon_orders", "success", total)

        inventory = await connector.get_inventory()
        inv_total = 0
        for item in inventory:
            sku = item.get("sellerSku", "")
            if not sku:
                continue
            qty = item.get("inventoryDetails", {}).get("fulfillableQuantity", 0)
            existing = db.query(InventoryItem).filter(InventoryItem.sku == sku).first()
            daily_sales = _calc_daily_sales(db, sku)
            doc = (qty / daily_sales) if daily_sales > 0 else 999.0
            if existing:
                existing.quantity_available = qty
                existing.asin = item.get("asin")
                existing.days_of_cover = doc
                existing.last_updated = datetime.utcnow()
            else:
                db.add(InventoryItem(
                    sku=sku,
                    asin=item.get("asin"),
                    title=item.get("productName", ""),
                    quantity_available=qty,
                    days_of_cover=doc,
                    last_updated=datetime.utcnow(),
                ))
            inv_total += 1
        db.commit()
        _log(db, "amazon_inventory", "success", inv_total)

    except Exception as e:
        logger.error("Amazon sync failed: %s", e)
        _log(db, "amazon", "error", 0, str(e))


async def sync_all():
    logger.info("Starting full sync at %s", datetime.utcnow())
    db = SessionLocal()
    try:
        await _sync_dropbox(db)
        await _sync_amazon(db)
        analyzer = AIAnalyzer()
        await analyzer.generate_full_analysis(db)
        logger.info("Full sync completed")
    except Exception as e:
        logger.error("sync_all failed: %s", e)
    finally:
        db.close()


def start_scheduler():
    interval = int(os.getenv("SYNC_INTERVAL_MINUTES", "60"))
    scheduler.add_job(sync_all, "interval", minutes=interval, id="sync_all", replace_existing=True)
    scheduler.start()
    logger.info("Scheduler started, sync interval: %d minutes", interval)
