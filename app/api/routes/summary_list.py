from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.models.summary import Summary
from app.models.call import Call


router = APIRouter(
    prefix="/api/summaries",
    tags=["Summary List"]
)


@router.get("")
def list_summaries(
    page: int = 1,
    size: int = 10,
    db: Session = Depends(get_db)
):

    query = (
        db.query(
            Summary,
            Call
        )
        .join(
            Call,
            Summary.call_id == Call.call_id
        )
    )

    total = query.count()

    rows = (
        query
        .offset((page - 1) * size)
        .limit(size)
        .all()
    )

    data = []

    for summary, call in rows:

        data.append({
            "summary_id": summary.summary_id,
            "summary_text": summary.summary_text,
            "call_type": call.call_type,
            "audio_path": f"/{summary.audio_summary_path}"
            if summary.audio_summary_path else None
        })

    return {
        "total": total,
        "page": page,
        "size": size,
        "items": data
    }