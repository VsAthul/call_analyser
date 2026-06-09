from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.models.transcript import Transcript

router = APIRouter(
    prefix="/api/calls",
    tags=["Transcript"]
)

@router.get("/{call_id}/transcript")
async def get_transcript(
    call_id: int,
    db: Session = Depends(get_db)
) -> dict:
    """
    Return transcript.
    """

    rows = (
        db.query(Transcript)
        .filter(
            Transcript.call_id == call_id
        )
        .all()
    )

    transcript_data: list[dict] = []

    for row in rows:

        transcript_data.append(
            {
                "speaker": row.speaker,
                "text": row.text
            }
        )

    return {
        "call_id": call_id,
        "transcript": transcript_data
    }