from pydantic import BaseModel


class UploadResponse(BaseModel):

    call_id: int
    status: str
    message: str
    call_type: str