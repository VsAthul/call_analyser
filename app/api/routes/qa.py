from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.models.qa import QAHistory

from app.schemas.qa_schema import (
    QuestionRequest
)

from app.services.rag_service import (
    answer_question
)

router = APIRouter(
    prefix="/api/calls",
    tags=["QA"]
)

@router.post("/{call_id}/ask")
async def ask_question(
    call_id: int,
    request: QuestionRequest,
    db: Session = Depends(get_db)
) -> dict:
    """
    Ask questions about call.
    """

    answer: str = answer_question(
        call_id=call_id,
        question=request.question
    )

    qa_row = QAHistory(
        call_id=call_id,
        question=request.question,
        answer=answer
    )

    db.add(qa_row)
    db.commit()

    return {
        "answer": answer
    }