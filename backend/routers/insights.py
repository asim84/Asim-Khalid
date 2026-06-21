import asyncio
import logging

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import AIInsight, SyncLog, get_db

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/insights", tags=["insights"])


class InsightResponse(BaseModel):
    id: int
    insight_type: str
    severity: str
    title: str
    description: str
    affected_skus: str | None
    generated_at: str
    is_read: bool


class SyncStatus(BaseModel):
    source: str
    status: str
    records_processed: int
    error_message: str | None
    synced_at: str


def _to_response(i: AIInsight) -> InsightResponse:
    return InsightResponse(
        id=i.id,
        insight_type=i.insight_type,
        severity=i.severity,
        title=i.title,
        description=i.description,
        affected_skus=i.affected_skus,
        generated_at=i.generated_at.isoformat(),
        is_read=i.is_read,
    )


@router.get("/", response_model=list[InsightResponse])
def get_insights(db: Session = Depends(get_db)):
    insights = (
        db.query(AIInsight)
        .order_by(AIInsight.is_read.asc(), AIInsight.generated_at.desc())
        .limit(50)
        .all()
    )
    return [_to_response(i) for i in insights]


@router.post("/{insight_id}/read")
def mark_read(insight_id: int, db: Session = Depends(get_db)):
    insight = db.query(AIInsight).filter(AIInsight.id == insight_id).first()
    if not insight:
        raise HTTPException(status_code=404, detail="Insight not found")
    insight.is_read = True
    db.commit()
    return {"status": "ok"}


async def _run_sync():
    from scheduler import sync_all
    await sync_all()


@router.post("/sync/trigger")
def trigger_sync(background_tasks: BackgroundTasks):
    background_tasks.add_task(asyncio.run, _run_sync())
    return {"status": "sync_triggered"}


@router.get("/sync/status", response_model=list[SyncStatus])
def get_sync_status(db: Session = Depends(get_db)):
    logs = (
        db.query(SyncLog)
        .order_by(SyncLog.synced_at.desc())
        .limit(10)
        .all()
    )
    return [
        SyncStatus(
            source=l.source,
            status=l.status,
            records_processed=l.records_processed,
            error_message=l.error_message,
            synced_at=l.synced_at.isoformat(),
        )
        for l in logs
    ]
