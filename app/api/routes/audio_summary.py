from pathlib import Path

from fastapi import APIRouter

from app.services.tts_service import (
    generate_audio_summary
)

from app.schemas.audio_summary_schema import (
    AudioSummaryRequest
)

router = APIRouter(
    prefix="/api/calls",
    tags=["Audio Summary"]
)

@router.post("/{call_id}/audio-summary")
async def create_audio_summary(
    call_id: int,
    request: AudioSummaryRequest
) -> dict:
    """
    Generate audio summary.
    """

    output_path: str = (
        f"generated_audio/"
        f"summary_{call_id}.mp3"
    )

    generate_audio_summary(
        summary=request.summary,
        output_path=output_path,
        language=request.language
    )

    return {
        "status": "generated",
        "audio_path": output_path
    }