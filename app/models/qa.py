from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import Text
from sqlalchemy import DateTime

from sqlalchemy.orm import relationship

from app.core.database import Base


class QAHistory(Base):

    __tablename__ = "qa_history"

    qa_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    call_id = Column(
        Integer,
        ForeignKey("calls.call_id")
    )

    question = Column(
        Text,
        nullable=False
    )

    answer = Column(
        Text,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    call = relationship(
        "Call",
        back_populates="qa_history"
    )