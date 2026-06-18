from pydantic import BaseModel
from typing import List, Literal

class UploadResponse(BaseModel):

    call_id: int
    status: str
    message: str
    call_type: str

class SpeakerSegment(BaseModel):
    speaker: str
    text: str

class SpeakerMapping(BaseModel):
    segments: List[SpeakerSegment]

class CallTypeResult(BaseModel):

    call_type: Literal[
        "Loan Inquiry",
        "Account Opening",
        "Account Issue",
        "Card Services",
        "Fraud Report",
        "Fund Transfer",
        "General Inquiry",
        "Complaint",
        "Technical Support"
    ]