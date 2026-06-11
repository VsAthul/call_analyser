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
from app.core.config import UPLOAD_FOLDER
from app.core.logger import logger

UPLOAD_FOLDER = UPLOAD_FOLDER

MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB

router = APIRouter(
    prefix="/api/calls",
    tags=["Calls"]
)


@router.post(
    "/upload",
    response_model=UploadResponse
)
async def upload_call(audio_file: UploadFile = File(...),
    db: Session = Depends(get_db)
) -> UploadResponse:
    """
    Upload and process audio.
    """
    logger.info(
    f"Upload request received. file={audio_file.filename}"
    )
    if not audio_file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file selected"
        )
    # Validate file size
    audio_file.file.seek(0, 2)
    file_size = audio_file.file.tell()
    audio_file.file.seek(0)

    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="Audio file exceeds 20 MB limit"
        )
    ALLOWED_EXTENSIONS = {
    ".wav",
    ".mp3",
    ".m4a",
    ".ogg",
    ".aac"
    }

    extension = Path(
        audio_file.filename
    ).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported audio format"
        )
    logger.info(
    f"File validated. file={audio_file.filename}, size={file_size}"
)

    # 1. Save file
    try:
        file_path: str = save_uploaded_file(
            file=audio_file,
            upload_folder=UPLOAD_FOLDER
        )
        logger.info(
        f"File saved successfully. path={file_path}"
    )

    except Exception as e:
        logger.exception(
        f"Failed to save file. file={audio_file.filename}"
    )
        raise HTTPException(
            status_code=500,
            detail=f"Unable to save file: {str(e)}"
        )

    # 2. Create call record with placeholder
    call: Call = Call(
        file_name=audio_file.filename,
        call_type="detecting...",
        audio_path=file_path,
        processing_status="processing"
    )

    try:
        db.add(call)
        db.commit()
        db.refresh(call)
        logger.info(
    f"Call record created. call_id={call.call_id}"
)

    except Exception:
        logger.exception(
        "Failed to create call record"
    )
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to create call record"
        )

    call_id: int = call.call_id

    # 3. Transcribe audio — segments carry start/end timestamps
    try:
        logger.info(
    f"Starting transcription. call_id={call_id}"
)
        transcript_segments: list[dict] = (
            await asyncio.to_thread(
                transcribe_audio,
                file_path
            )
        )
        logger.info(
    f"Transcription completed. call_id={call_id}, segments={len(transcript_segments)}"
)

    except Exception as e:
        logger.exception(
        f"Transcription failed. call_id={call_id}"
    )
        raise HTTPException(
            status_code=500,
            detail=f"Transcription failed: {str(e)}"
        )

    if not transcript_segments:
        raise HTTPException(
            status_code=400,
            detail="No speech detected in audio"
        )

    # before timing data is lost in the speaker-mapping step.
    duration_seconds: float | None = None

    if transcript_segments:
        duration_seconds = (
    transcript_segments[-1].get("end")
)

    # 4. Map speakers
    try:
        logger.info(
    f"Starting speaker mapping. call_id={call_id}"
)
        speaker_mapped_segments: list[dict] = (
            await asyncio.to_thread(
                map_speakers,
                transcript_segments
            )
        )
        logger.info(
        f"Speaker mapping completed. call_id={call_id}"
    )

    except Exception as e:
        logger.exception(
        f"Speaker mapping failed. call_id={call_id}"
    )
        raise HTTPException(
            status_code=500,
            detail=f"Speaker mapping failed: {str(e)}"
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

    try:
        db.commit()
        logger.info(
    f"Transcript saved. call_id={call_id}"
)

    except Exception:
        logger.exception(
        f"Failed to save transcript. call_id={call_id}"
    )
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Failed to save transcript"
        )

    # 6. Build transcript text
    transcript_text: str = transcript_to_text(
        speaker_mapped_segments
    )

    # 7. Detect call type using LLM
    try:
        logger.info(
    f"Detecting call type. call_id={call_id}"
)
        detected_call_type: str = (
            await asyncio.to_thread(
                detect_call_type,
                transcript_text
            )
        )
        logger.info(
    f"Call type detected. call_id={call_id}, type={detected_call_type}"
)

    except Exception:
        logger.exception(
        f"Call type detection failed. call_id={call_id}"
    )
        detected_call_type = "General Inquiry"

    # 8. Store chunks in ChromaDB
    chunks: list[str] = chunk_text(
        transcript_text
    )

    try:
        logger.info(
    f"Storing chunks in ChromaDB. call_id={call_id}, chunks={len(chunks)}"
)
        await asyncio.to_thread(
            store_chunks,
            call_id=call_id,
            chunks=chunks
        )
        logger.info(
    f"Chunks stored successfully. call_id={call_id}"
)
    except Exception as e:
        logger.exception(
        f"Vector indexing failed. call_id={call_id}"
    )
        raise HTTPException(
            status_code=500,
            detail=f"Vector indexing failed: {str(e)}"
        )

    # 9. Update call record
    call = (
        db.query(Call)
        .filter(
            Call.call_id == call_id
        )
        .first()
    )
    if not call:
        raise HTTPException(
            status_code=404,
            detail="Call record not found"
        )
    call.call_type = detected_call_type
    call.processing_status = "completed"
    call.duration_seconds = duration_seconds

    try:
        db.commit()
        logger.info(
    f"Call processing completed. call_id={call_id}"
)

    except Exception:
        logger.exception(
        f"Failed to update call status. call_id={call_id}"
    )

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Failed to update call status"
        )

    return UploadResponse(
        call_id=call_id,
        status="completed",
        message="Call processed successfully",
        call_type=detected_call_type
    )