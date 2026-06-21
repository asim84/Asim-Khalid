import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import SessionLocal, init_db
from routers import fees, insights, inventory, sales
from scheduler import start_scheduler

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    logger.info("Database initialised")
    start_scheduler()
    yield
    from scheduler import scheduler
    if scheduler.running:
        scheduler.shutdown()


app = FastAPI(title="BizAI", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sales.router)
app.include_router(inventory.router)
app.include_router(fees.router)
app.include_router(insights.router)


@app.get("/api/health")
def health_check():
    from datetime import datetime
    db = SessionLocal()
    try:
        from database import SyncLog
        last = db.query(SyncLog).order_by(SyncLog.synced_at.desc()).first()
        return {
            "status": "ok",
            "db": "ok",
            "last_sync": last.synced_at.isoformat() if last else None,
        }
    finally:
        db.close()
