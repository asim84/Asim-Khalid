import asyncio
import logging
import os
import time
from datetime import datetime, timedelta
from typing import Any, Optional

import httpx

logger = logging.getLogger(__name__)

AMAZON_TOKEN_URL = "https://api.amazon.com/auth/o2/token"
AMAZON_SP_API_BASE = "https://sellingpartnerapi-eu.amazon.com"


class AmazonConnector:
    def __init__(self):
        self.refresh_token = os.getenv("AMAZON_REFRESH_TOKEN", "")
        self.client_id = os.getenv("AMAZON_CLIENT_ID", "")
        self.client_secret = os.getenv("AMAZON_CLIENT_SECRET", "")
        self.marketplace_id = os.getenv("AMAZON_MARKETPLACE_ID", "A1F83G8C2ARO7P")
        self._access_token: Optional[str] = None
        self._token_expires_at: float = 0.0

    async def get_access_token(self) -> str:
        """Get a valid access token, refreshing if necessary."""
        now = time.time()
        if self._access_token and now < self._token_expires_at:
            return self._access_token

        async with httpx.AsyncClient() as client:
            response = await client.post(
                AMAZON_TOKEN_URL,
                data={
                    "grant_type": "refresh_token",
                    "refresh_token": self.refresh_token,
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                },
            )
            response.raise_for_status()
            data = response.json()
            self._access_token = data["access_token"]
            self._token_expires_at = now + 3500  # Cache for 3500 seconds
            logger.info("Amazon access token refreshed")
            return self._access_token

    async def _make_request(
        self,
        method: str,
        path: str,
        params: Optional[dict] = None,
        max_retries: int = 3,
    ) -> Any:
        """Make an authenticated request to the SP-API with retry on 429."""
        token = await self.get_access_token()
        headers = {
            "x-amz-access-token": token,
            "Content-Type": "application/json",
        }
        url = f"{AMAZON_SP_API_BASE}{path}"

        for attempt in range(max_retries):
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.request(
                    method, url, headers=headers, params=params
                )
                if response.status_code == 429:
                    wait = 2 ** attempt
                    logger.warning(f"Rate limited by Amazon SP-API, waiting {wait}s")
                    await asyncio.sleep(wait)
                    continue
                response.raise_for_status()
                return response.json()

        raise RuntimeError(f"Failed to complete request to {path} after {max_retries} retries")

    async def get_orders(self, days_back: int = 7) -> list[dict]:
        """Fetch recent orders from Amazon SP-API."""
        created_after = (datetime.utcnow() - timedelta(days=days_back)).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        )
        params = {
            "MarketplaceIds": self.marketplace_id,
            "CreatedAfter": created_after,
            "OrderStatuses": "Shipped",
        }
        try:
            data = await self._make_request("GET", "/orders/v0/orders", params=params)
            orders = data.get("payload", {}).get("Orders", [])
            logger.info(f"Fetched {len(orders)} orders from Amazon")
            return orders
        except Exception as e:
            logger.error(f"Failed to fetch Amazon orders: {e}")
            return []

    async def get_inventory(self) -> list[dict]:
        """Fetch FBA inventory summaries from Amazon SP-API."""
        params = {
            "details": "true",
            "granularityType": "Marketplace",
            "granularityId": self.marketplace_id,
            "marketplaceIds": self.marketplace_id,
        }
        try:
            data = await self._make_request(
                "GET", "/fba/inventory/v1/summaries", params=params
            )
            summaries = data.get("payload", {}).get("inventorySummaries", [])
            logger.info(f"Fetched {len(summaries)} inventory items from Amazon")
            return summaries
        except Exception as e:
            logger.error(f"Failed to fetch Amazon inventory: {e}")
            return []

    async def get_financial_events(self, order_id: str) -> list[dict]:
        """Fetch financial events for a specific order."""
        try:
            data = await self._make_request(
                "GET", f"/finances/v0/orders/{order_id}/financialEvents"
            )
            events = data.get("payload", {}).get("FinancialEvents", {})
            logger.info(f"Fetched financial events for order {order_id}")
            return events if isinstance(events, list) else [events]
        except Exception as e:
            logger.error(f"Failed to fetch financial events for {order_id}: {e}")
            return []
