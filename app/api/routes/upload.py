from pathlib import Path
import asyncio

from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.models.call import Call
from app.models.transcript import Transcript

from app.schemas.upload_schema import UploadResponse

from app.utils.file_utils import save_uploaded_file
from app.utils.chunking import chunk_text

from app.services.whisper_service import transcribe_audio
from app.services.speaker_service import map_speakers
from app.services.transcript_service import transcript_to_text
from app.services.chroma_service import store_chunks
from app.services.summary_service import detect_call_type

UPLOAD_FOLDER = "uploads"

MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB

router = APIRouter(
    prefix="/api/calls",
    tags=["Calls"]
)


@router.post(
    "/upload",
    response_model=UploadResponse
)
async def upload_call(
    audio_file: UploadFile = File(...),
    db: Session = Depends(get_db)
) -> UploadResponse:
    """
    Upload and process audio.
    """

    # Validate file size
    audio_file.file.seek(0, 2)
    file_size = audio_file.file.tell()
    audio_file.file.seek(0)

    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="Audio file exceeds 20 MB limit"
        )

    # 1. Save file
    file_path: str = save_uploaded_file(
        file=audio_file,
        upload_folder=UPLOAD_FOLDER
    )

    # 2. Create call record with placeholder
    call: Call = Call(
        file_name=audio_file.filename,
        call_type="detecting...",
        audio_path=file_path,
        processing_status="processing"
    )

    db.add(call)
    db.commit()
    db.refresh(call)

    call_id: int = call.call_id

    # 3. Transcribe audio — segments carry start/end timestamps
    transcript_segments: list[dict] = await asyncio.to_thread(
        transcribe_audio,
        file_path
    )

    # before timing data is lost in the speaker-mapping step.
    duration_seconds: float | None = None

    if transcript_segments:
        duration_seconds = transcript_segments[-1]["end"]

    # 4. Map speakers
    speaker_mapped_segments: list[dict] = await asyncio.to_thread(
        map_speakers,
        transcript_segments
    )

    # 5. Save transcript rows
    for i, item in enumerate(
        speaker_mapped_segments
    ):

        original = (
            transcript_segments[i]
            if i < len(transcript_segments)
            else {}
        )

        start: float | None = original.get(
            "start"
        )

        end: float | None = original.get(
            "end"
        )

        if (
            start is not None
            and end is not None
        ):
            timestamp: str | None = (
                f"{start:.2f}s - {end:.2f}s"
            )
        else:
            timestamp = None

        db.add(
            Transcript(
                call_id=call_id,
                speaker=item["speaker"],
                text=item["text"],
                timestamp=timestamp
            )
        )

    db.commit()

    # 6. Build transcript text
    transcript_text: str = transcript_to_text(
        speaker_mapped_segments
    )

    # 7. Detect call type using LLM
    detected_call_type: str = await asyncio.to_thread(
        detect_call_type,
        transcript_text
    )

    # 8. Store chunks in ChromaDB
    chunks: list[str] = chunk_text(
        transcript_text
    )

    await asyncio.to_thread(
        store_chunks,
        call_id=call_id,
        chunks=chunks
    )

    # 9. Update call record
    call = (
        db.query(Call)
        .filter(
            Call.call_id == call_id
        )
        .first()
    )

    call.call_type = detected_call_type
    call.processing_status = "completed"
    call.duration_seconds = duration_seconds

    db.commit()

    return UploadResponse(
        call_id=call_id,
        status="completed",
        message="Call processed successfully",
        call_type=detected_call_type
    )