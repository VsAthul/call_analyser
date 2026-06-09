from pathlib import Path

from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File
from fastapi import Form
from fastapi import Depends

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

UPLOAD_FOLDER = "uploads"
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
    call_type: str = Form(...),
    db: Session = Depends(get_db)
) -> UploadResponse:
    """
    Upload and process audio.
    """

    file_path: str = save_uploaded_file(
        file=audio_file,
        upload_folder=UPLOAD_FOLDER
    )

    call: Call = Call(
        file_name=audio_file.filename,
        call_type=call_type,
        audio_path=file_path,
        processing_status="processing"
    )

    db.add(call)
    db.commit()
    db.refresh(call)

    transcript_segments: list[dict] = (
        transcribe_audio(file_path)
    )

    speaker_mapped_segments: list[dict] = (
        map_speakers(
            transcript_segments
        )
    )

    for item in speaker_mapped_segments:

        transcript_row: Transcript = (
            Transcript(
                call_id=call.call_id,
                speaker=item["speaker"],
                text=item["text"]
            )
        )

        db.add(transcript_row)

    db.commit()

    transcript_text: str = (
        transcript_to_text(
            speaker_mapped_segments
        )
    )

    chunks: list[str] = (
        chunk_text(
            transcript_text
        )
    )

    store_chunks(
        call_id=call.call_id,
        chunks=chunks
    )

    call.processing_status = (
        "completed"
    )

    db.commit()

    return UploadResponse(
        call_id=call.call_id,
        status="completed",
        message="Call processed successfully"
    )