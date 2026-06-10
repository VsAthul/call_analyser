from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.models.transcript import Transcript
from app.models.summary import Summary

from app.services.summary_service import generate_summary
from app.services.tts_service import generate_audio_summary


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
    Generate summary and audio summary.
    """

    existing_summary = (
        db.query(Summary)
        .filter(
            Summary.call_id == call_id
        )
        .first()
    )

    if existing_summary:
        return {
            "call_id": call_id,
            "summary": existing_summary.summary_text,
            "audio_path":
                f"/{existing_summary.audio_summary_path}"
                if existing_summary.audio_summary_path
                else None
        }

    rows = (
        db.query(Transcript)
        .filter(
            Transcript.call_id == call_id
        )
        .all()
    )

    if not rows:
        return {
            "error": "Transcript not found"
        }

    transcript_text = "\n".join(
        [
            f"{row.speaker}: {row.text}"
            for row in rows
        ]
    )

    summary_text = generate_summary(
        transcript_text
    )

    audio_path = (
        f"generated_audio/"
        f"summary_{call_id}.mp3"
    )

    generate_audio_summary(
        summary=summary_text,
        output_path=audio_path,
        language="en"
    )

    summary = Summary(
        call_id=call_id,
        summary_text=summary_text,
        audio_summary_path=audio_path
    )

    db.add(summary)
    db.commit()
    db.refresh(summary)

    return {
        "call_id": call_id,
        "summary": summary_text,
        "audio_path": f"/{audio_path}"
    }