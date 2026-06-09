from pydantic import BaseModel


class TranscriptItem(BaseModel):

    speaker: str
    text: str


class TranscriptResponse(BaseModel):

    call_id: int
    transcript: list[TranscriptItem]