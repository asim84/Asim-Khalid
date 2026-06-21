import io
import logging
from typing import Any

import pandas as pd

logger = logging.getLogger(__name__)

# Column name mappings for orders
ORDER_COLUMN_MAP = {
    "order_id": ["OrderId", "Order ID", "order_id", "OrderID", "Reference", "NumOrderId"],
    "sku": ["SKU", "Sku", "sku", "StockItemNumber", "Item SKU"],
    "title": ["Title", "ItemTitle", "ProductTitle", "Item Title", "StockTitle", "Description"],
    "quantity": ["Quantity", "Qty", "quantity", "Units", "NumItems", "ItemQuantity"],
    "revenue": ["Revenue", "Price", "OrderTotal", "Total", "ItemPrice", "GrossRevenue", "SalePrice"],
    "currency": ["Currency", "CurrencyCode"],
    "order_date": ["OrderDate", "Order Date", "Date", "CreatedDate", "PurchaseDate"],
    "status": ["Status", "OrderStatus", "FulfillmentStatus"],
    "marketplace": ["Marketplace", "Source", "Channel", "Site"],
}

# Column name mappings for inventory
INVENTORY_COLUMN_MAP = {
    "sku": ["SKU", "Sku", "sku", "StockItemNumber", "ItemSKU"],
    "title": ["Title", "ItemTitle", "ProductTitle", "StockTitle", "Description", "Name"],
    "quantity_available": ["Available", "QuantityAvailable", "StockLevel", "InStock", "Qty Available"],
    "quantity_inbound": ["Inbound", "QuantityInbound", "InboundQty", "PendingInbound"],
    "quantity_reserved": ["Reserved", "QuantityReserved", "ReservedQty"],
    "reorder_point": ["ReorderPoint", "ReorderLevel", "MinStock", "MinQty"],
    "cost_price": ["CostPrice", "Cost", "UnitCost", "CostPerUnit"],
    "sell_price": ["SellPrice", "Price", "RetailPrice", "ListPrice", "SalePrice"],
    "asin": ["ASIN", "Asin", "asin"],
}


def _find_column(df: pd.DataFrame, candidates: list[str]) -> str | None:
    """Find the first matching column from a list of candidates."""
    for col in candidates:
        if col in df.columns:
            return col
    # Case-insensitive fallback
    lower_cols = {c.lower(): c for c in df.columns}
    for col in candidates:
        if col.lower() in lower_cols:
            return lower_cols[col.lower()]
    return None


def _safe_int_pence(value: Any, default: int = 0) -> int:
    """Convert a value (possibly with currency symbols) to pence."""
    try:
        if isinstance(value, str):
            value = value.replace("£", "").replace("$", "").replace(",", "").strip()
        return int(round(float(value) * 100))
    except (ValueError, TypeError):
        return default


def parse_orders_csv(content: bytes) -> list[dict]:
    """Parse a Linnworks orders CSV export and return normalized order dicts."""
    try:
        df = pd.read_csv(io.BytesIO(content), encoding="utf-8-sig")
    except Exception:
        df = pd.read_csv(io.BytesIO(content), encoding="latin-1")

    df.columns = df.columns.str.strip()
    logger.info(f"Parsing orders CSV with columns: {list(df.columns)}")

    orders = []
    for _, row in df.iterrows():
        order: dict[str, Any] = {}

        col = _find_column(df, ORDER_COLUMN_MAP["order_id"])
        order["order_id"] = str(row[col]).strip() if col else f"LW-{_}"

        col = _find_column(df, ORDER_COLUMN_MAP["sku"])
        order["sku"] = str(row[col]).strip() if col else "UNKNOWN"

        col = _find_column(df, ORDER_COLUMN_MAP["title"])
        order["title"] = str(row[col]).strip() if col else ""

        col = _find_column(df, ORDER_COLUMN_MAP["quantity"])
        try:
            order["quantity"] = int(row[col]) if col else 1
        except (ValueError, TypeError):
            order["quantity"] = 1

        col = _find_column(df, ORDER_COLUMN_MAP["revenue"])
        order["revenue_pence"] = _safe_int_pence(row[col] if col else 0)

        col = _find_column(df, ORDER_COLUMN_MAP["currency"])
        order["currency"] = str(row[col]).strip() if col else "GBP"

        col = _find_column(df, ORDER_COLUMN_MAP["order_date"])
        try:
            order["order_date"] = pd.to_datetime(row[col]).to_pydatetime() if col else None
        except Exception:
            order["order_date"] = None

        col = _find_column(df, ORDER_COLUMN_MAP["status"])
        order["status"] = str(row[col]).strip() if col else "Shipped"

        col = _find_column(df, ORDER_COLUMN_MAP["marketplace"])
        order["marketplace"] = str(row[col]).strip() if col else "UK"

        order["source"] = "linnworks"
        orders.append(order)

    logger.info(f"Parsed {len(orders)} orders from CSV")
    return orders


def parse_inventory_csv(content: bytes) -> list[dict]:
    """Parse a Linnworks inventory CSV export and return normalized inventory dicts."""
    try:
        df = pd.read_csv(io.BytesIO(content), encoding="utf-8-sig")
    except Exception:
        df = pd.read_csv(io.BytesIO(content), encoding="latin-1")

    df.columns = df.columns.str.strip()
    logger.info(f"Parsing inventory CSV with columns: {list(df.columns)}")

    items = []
    for _, row in df.iterrows():
        item: dict[str, Any] = {}

        col = _find_column(df, INVENTORY_COLUMN_MAP["sku"])
        item["sku"] = str(row[col]).strip() if col else f"SKU-{_}"

        col = _find_column(df, INVENTORY_COLUMN_MAP["title"])
        item["title"] = str(row[col]).strip() if col else ""

        col = _find_column(df, INVENTORY_COLUMN_MAP["asin"])
        item["asin"] = str(row[col]).strip() if col else None

        col = _find_column(df, INVENTORY_COLUMN_MAP["quantity_available"])
        try:
            item["quantity_available"] = int(row[col]) if col else 0
        except (ValueError, TypeError):
            item["quantity_available"] = 0

        col = _find_column(df, INVENTORY_COLUMN_MAP["quantity_inbound"])
        try:
            item["quantity_inbound"] = int(row[col]) if col else 0
        except (ValueError, TypeError):
            item["quantity_inbound"] = 0

        col = _find_column(df, INVENTORY_COLUMN_MAP["quantity_reserved"])
        try:
            item["quantity_reserved"] = int(row[col]) if col else 0
        except (ValueError, TypeError):
            item["quantity_reserved"] = 0

        col = _find_column(df, INVENTORY_COLUMN_MAP["reorder_point"])
        try:
            item["reorder_point"] = int(row[col]) if col else 10
        except (ValueError, TypeError):
            item["reorder_point"] = 10

        col = _find_column(df, INVENTORY_COLUMN_MAP["cost_price"])
        item["cost_price_pence"] = _safe_int_pence(row[col] if col else 0)

        col = _find_column(df, INVENTORY_COLUMN_MAP["sell_price"])
        item["sell_price_pence"] = _safe_int_pence(row[col] if col else 0)

        items.append(item)

    logger.info(f"Parsed {len(items)} inventory items from CSV")
    return items


def detect_export_type(filename: str) -> str:
    """Detect whether a CSV file is an orders or inventory export based on filename."""
    lower = filename.lower()
    if any(keyword in lower for keyword in ["order", "sale", "dispatch", "shipped"]):
        return "orders"
    if any(keyword in lower for keyword in ["inventory", "stock", "invent", "product"]):
        return "inventory"
    return "unknown"
