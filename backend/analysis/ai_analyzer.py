import json
import logging
from datetime import datetime
from typing import Any

import anthropic
from sqlalchemy.orm import Session

from database import AIInsight, FeeRecord, InventoryItem, Order

logger = logging.getLogger(__name__)

MODEL = "claude-sonnet-4-6"

SYSTEM_PROMPT = """You are a business intelligence analyst for an e-commerce seller.
Analyse the provided data and return a JSON array of insights.
Each insight must be a JSON object with these exact fields:
- type: string (e.g. "sales_trend", "inventory_health", "fee_analysis")
- severity: "info" | "warning" | "critical"
- title: short string (max 80 chars)
- description: detailed string explaining the issue and recommended action
- affected_skus: comma-separated string of SKU codes, or null if not applicable

Return ONLY the JSON array, no markdown, no explanation."""


class AIAnalyzer:
    def __init__(self):
        self.client = anthropic.Anthropic()

    def _call_claude(self, prompt: str) -> list[dict]:
        """Call Claude and parse the JSON response."""
        try:
            message = self.client.messages.create(
                model=MODEL,
                max_tokens=4096,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": prompt}],
            )
            content = message.content[0].text.strip()
            # Strip markdown code blocks if present
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
            return json.loads(content)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Claude response as JSON: {e}")
            return []
        except Exception as e:
            logger.error(f"Claude API call failed: {e}")
            return []

    async def analyze_sales_trends(self, orders: list[dict]) -> list[dict]:
        """Analyse sales orders to detect trends, drops, spikes, and top/bottom performers."""
        if not orders:
            return []

        prompt = f"""Analyse these e-commerce sales orders and identify:
1. Revenue trends (drops or spikes of >20% week-over-week)
2. Top 3 performing SKUs by revenue
3. Bottom 3 performing SKUs by revenue (that had sales)
4. Any SKUs with declining sales over the last 4 weeks
5. Any unusual patterns worth flagging

Orders data (last 90 days, revenue in pence):
{json.dumps(orders[:500], default=str, indent=2)}

Return a JSON array of insight objects."""

        return self._call_claude(prompt)

    async def analyze_inventory_health(self, inventory: list[dict]) -> list[dict]:
        """Analyse inventory levels to flag low stock and overstock situations."""
        if not inventory:
            return []

        prompt = f"""Analyse this inventory data and identify:
1. Items critically low in stock (days_of_cover < 7)
2. Items running low (days_of_cover between 7-14)
3. Overstocked items (days_of_cover > 90 and quantity_available > 100)
4. Items below their reorder point
5. Items with 0 stock that were selling recently

Inventory data:
{json.dumps(inventory, default=str, indent=2)}

Return a JSON array of insight objects."""

        return self._call_claude(prompt)

    async def analyze_fees(self, fees: list[dict], orders: list[dict]) -> list[dict]:
        """Analyse fee records to flag spikes or unusually high fee percentages."""
        if not fees:
            return []

        # Compute fee percentage per SKU
        sku_revenue: dict[str, int] = {}
        for order in orders:
            sku = order.get("sku", "UNKNOWN")
            sku_revenue[sku] = sku_revenue.get(sku, 0) + order.get("revenue_pence", 0)

        prompt = f"""Analyse these fee records for an Amazon/Linnworks seller and identify:
1. SKUs where total fees exceed 30% of revenue
2. Fee types that have increased significantly
3. Any unexpected fee charges (unusual fee types)
4. Overall fee trend — are fees growing faster than revenue?

Fee records (amounts in pence):
{json.dumps(fees[:300], default=str, indent=2)}

SKU revenue totals (pence):
{json.dumps(sku_revenue, indent=2)}

Return a JSON array of insight objects."""

        return self._call_claude(prompt)

    async def generate_full_analysis(self, db_session: Session) -> list[AIInsight]:
        """Run all analyses, save insights to DB, and return new insights."""
        # Fetch data
        orders = db_session.query(Order).order_by(Order.order_date.desc()).limit(500).all()
        inventory = db_session.query(InventoryItem).all()
        fees = db_session.query(FeeRecord).order_by(FeeRecord.recorded_at.desc()).limit(300).all()

        orders_data = [
            {
                "order_id": o.order_id,
                "sku": o.sku,
                "title": o.title,
                "quantity": o.quantity,
                "revenue_pence": o.revenue_pence,
                "fees_pence": o.fees_pence,
                "net_profit_pence": o.net_profit_pence,
                "order_date": o.order_date.isoformat() if o.order_date else None,
                "marketplace": o.marketplace,
            }
            for o in orders
        ]

        inventory_data = [
            {
                "sku": i.sku,
                "title": i.title,
                "quantity_available": i.quantity_available,
                "quantity_inbound": i.quantity_inbound,
                "reorder_point": i.reorder_point,
                "days_of_cover": i.days_of_cover,
                "sell_price_pence": i.sell_price_pence,
                "cost_price_pence": i.cost_price_pence,
            }
            for i in inventory
        ]

        fees_data = [
            {
                "order_id": f.order_id,
                "fee_type": f.fee_type,
                "amount_pence": f.amount_pence,
            }
            for f in fees
        ]

        # Run all analyses
        all_raw_insights: list[dict[str, Any]] = []
        all_raw_insights.extend(await self.analyze_sales_trends(orders_data))
        all_raw_insights.extend(await self.analyze_inventory_health(inventory_data))
        all_raw_insights.extend(await self.analyze_fees(fees_data, orders_data))

        # Persist to DB
        new_insights: list[AIInsight] = []
        for raw in all_raw_insights:
            if not isinstance(raw, dict):
                continue
            insight = AIInsight(
                insight_type=raw.get("type", "general"),
                severity=raw.get("severity", "info"),
                title=raw.get("title", "Insight")[:255],
                description=raw.get("description", ""),
                affected_skus=raw.get("affected_skus"),
                generated_at=datetime.utcnow(),
                is_read=False,
            )
            db_session.add(insight)
            new_insights.append(insight)

        db_session.commit()
        logger.info(f"Generated and saved {len(new_insights)} AI insights")
        return new_insights
