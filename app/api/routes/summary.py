from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.models.transcript import Transcript
from app.models.summary import Summary

from app.services.summary_service import (
    generate_summary
)

router = APIRouter(
    prefix="/api/calls",
    tags=["Summary"]
)

@router.get("/{call_id}/summary")
async def get_summary(
    call_id: int,
    db: Session = Depends(get_db)
) -> dict:
    """
    Generate summary.
    """

    rows = (
        db.query(Transcript)
        .filter(
            Transcript.call_id == call_id
        )
        .all()
    )

    transcript_text: str = "\n".join(
        [
            f"{row.speaker}: {row.text}"
            for row in rows
        ]
    )

    summary_text: str = (
        generate_summary(
            transcript_text
        )
    )

    summary = Summary(
        call_id=call_id,
        summary_text=summary_text
    )

    db.add(summary)
    db.commit()

    return {
        "call_id": call_id,
        "summary": summary_text
    }