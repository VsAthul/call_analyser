from pydantic import BaseModel


class AudioSummaryRequest(BaseModel):

    summary: str
    voice: str = "male"
    language: str = "en"


class AudioSummaryResponse(BaseModel):

    audio_summary_id: int
    status: str
    audio_path: str