"""
Run this script to populate the database with realistic demo data.
Usage: python seed_data.py
"""
import random
from datetime import datetime, timedelta

from database import AIInsight, FeeRecord, InventoryItem, Order, SessionLocal, init_db

SKUS = [
    ("SKU-001", "Premium Wireless Headphones", "B08X1Y2Z3A"),
    ("SKU-002", "Ergonomic Office Chair Cushion", "B07Y3Z4A5B"),
    ("SKU-003", "Bamboo Cutting Board Set", "B09Z4A5B6C"),
    ("SKU-004", "LED Desk Lamp USB-C", "B08A5B6C7D"),
    ("SKU-005", "Stainless Steel Water Bottle 1L", "B07B6C7D8E"),
    ("SKU-006", "Yoga Mat Non-Slip 6mm", "B09C7D8E9F"),
    ("SKU-007", "Digital Kitchen Scale 5kg", "B08D8E9F0G"),
    ("SKU-008", "Phone Stand Adjustable", "B07E9F0G1H"),
    ("SKU-009", "Reusable Shopping Bags (5 Pack)", "B09F0G1H2I"),
    ("SKU-010", "Silicone Baking Mat Set", "B08G1H2I3J"),
    ("SKU-011", "Cable Management Box", "B07H2I3J4K"),
    ("SKU-012", "Portable Phone Charger 20000mAh", "B09I3J4K5L"),
    ("SKU-013", "Wooden Coat Hangers (10 Pack)", "B08J4K5L6M"),
    ("SKU-014", "Foldable Storage Boxes (3 Pack)", "B07K5L6M7N"),
    ("SKU-015", "Garden Tool Set 5-Piece", "B09L6M7N8O"),
]

SELL_PRICES = [2999, 3499, 1999, 3999, 1799, 4499, 2499, 1299, 1099, 1599, 2299, 5999, 799, 1499, 3299]
COST_PRICES = [1200, 1500, 800, 1700, 700, 1900, 1000, 500, 400, 600, 900, 2500, 300, 600, 1400]
DAILY_VELOCITIES = [3.5, 2.1, 4.0, 1.8, 5.2, 1.2, 2.8, 6.1, 4.5, 3.3, 1.5, 0.9, 7.2, 3.8, 1.1]
STOCK_LEVELS = [24, 150, 5, 88, 3, 201, 42, 2, 67, 110, 30, 8, 14, 55, 92]

SOURCES = ["amazon", "linnworks", "amazon"]
MARKETPLACES = ["Amazon UK", "eBay UK", "Amazon DE"]
FEE_TYPES = ["Referral Fee", "FBA Fulfillment Fee", "Closing Fee", "Variable Closing Fee", "FBA Storage Fee"]


def random_order_date(days_back_max=90):
    return datetime.utcnow() - timedelta(days=random.uniform(0, days_back_max), hours=random.uniform(0, 24))


def main():
    init_db()
    db = SessionLocal()

    print("Seeding inventory...")
    for i, (sku, title, asin) in enumerate(SKUS):
        qty = STOCK_LEVELS[i]
        vel = DAILY_VELOCITIES[i]
        doc = qty / vel if vel > 0 else 999.0
        item = InventoryItem(
            sku=sku,
            asin=asin,
            title=title,
            quantity_available=qty,
            quantity_inbound=random.randint(0, 50),
            quantity_reserved=random.randint(0, 10),
            reorder_point=15,
            cost_price_pence=COST_PRICES[i],
            sell_price_pence=SELL_PRICES[i],
            days_of_cover=round(doc, 1),
            last_updated=datetime.utcnow(),
        )
        db.merge(item)
    db.commit()
    print(f"  Created {len(SKUS)} inventory items")

    print("Seeding orders...")
    order_count = 0
    for day_offset in range(90):
        date = datetime.utcnow() - timedelta(days=day_offset)
        for i, (sku, title, _) in enumerate(SKUS):
            daily_vel = DAILY_VELOCITIES[i]
            num_orders = max(0, int(random.gauss(daily_vel, daily_vel * 0.3)))
            for _ in range(num_orders):
                source_idx = random.randint(0, 2)
                source = SOURCES[source_idx]
                marketplace = MARKETPLACES[source_idx]
                qty = random.randint(1, 3)
                revenue = SELL_PRICES[i] * qty
                referral = int(revenue * 0.15)
                fba = 350 * qty
                total_fees = referral + fba
                net = revenue - total_fees - (COST_PRICES[i] * qty)

                order = Order(
                    source=source,
                    marketplace=marketplace,
                    order_id=f"{source.upper()}-{day_offset:03d}-{i:02d}-{order_count:05d}",
                    sku=sku,
                    asin=SKUS[i][2],
                    title=title,
                    quantity=qty,
                    revenue_pence=revenue,
                    currency="GBP",
                    fees_pence=total_fees,
                    net_profit_pence=net,
                    order_date=date - timedelta(hours=random.uniform(0, 20)),
                    status="Shipped",
                )
                db.add(order)

                fee_order_id = order.order_id
                db.add(FeeRecord(order_id=fee_order_id, fee_type="Referral Fee", amount_pence=referral, recorded_at=order.order_date))
                db.add(FeeRecord(order_id=fee_order_id, fee_type="FBA Fulfillment Fee", amount_pence=fba, recorded_at=order.order_date))
                if random.random() < 0.1:
                    storage = random.randint(10, 100)
                    db.add(FeeRecord(order_id=fee_order_id, fee_type="FBA Storage Fee", amount_pence=storage, recorded_at=order.order_date))

                order_count += 1

    db.commit()
    print(f"  Created {order_count} orders with fee records")

    print("Seeding AI insights...")
    sample_insights = [
        AIInsight(insight_type="inventory_health", severity="critical", title="SKU-001 critically low: 24 units, 6.9 days cover", description="Premium Wireless Headphones (SKU-001) has only 6.9 days of stock cover remaining at current sales velocity of 3.5 units/day. Immediate reorder recommended to avoid stockout.", affected_skus="SKU-001", generated_at=datetime.utcnow(), is_read=False),
        AIInsight(insight_type="inventory_health", severity="critical", title="SKU-005 near stockout: 3 units remaining", description="Stainless Steel Water Bottle (SKU-005) has only 3 units left with a daily velocity of 5.2 units. Stockout expected within 1 day. Place emergency order.", affected_skus="SKU-005", generated_at=datetime.utcnow(), is_read=False),
        AIInsight(insight_type="inventory_health", severity="warning", title="SKU-006 overstocked: 201 units, 167 days cover", description="Yoga Mat (SKU-006) has 201 units with only 1.2 units/day velocity — 167 days of cover. Consider promotional pricing or bundle deals to accelerate sell-through and reduce FBA storage fees.", affected_skus="SKU-006", generated_at=datetime.utcnow(), is_read=False),
        AIInsight(insight_type="sales_trend", severity="info", title="SKU-008 is top performer: 6.1 units/day average", description="Phone Stand Adjustable (SKU-008) is the highest-velocity SKU at 6.1 units/day. Consider increasing stock depth and exploring bundling opportunities.", affected_skus="SKU-008", generated_at=datetime.utcnow(), is_read=True),
        AIInsight(insight_type="fee_analysis", severity="warning", title="FBA fees consuming 17.5% of revenue on average", description="Average FBA fulfillment + referral fees are 17.5% of gross revenue. Review pricing strategy for lower-margin SKUs (SKU-009, SKU-013) where net margin may be below 10%.", affected_skus="SKU-009,SKU-013", generated_at=datetime.utcnow(), is_read=False),
    ]
    for insight in sample_insights:
        db.add(insight)
    db.commit()
    print(f"  Created {len(sample_insights)} AI insights")

    db.close()
    print("\nSeed complete. Run the backend and open the dashboard.")


if __name__ == "__main__":
    main()
