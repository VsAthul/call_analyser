from pydantic import BaseModel


class SummaryResponse(BaseModel):

    call_id: int
    summary: str
    
class SummaryResult(BaseModel):
    summary: str