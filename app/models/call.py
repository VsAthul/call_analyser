from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import DateTime

from sqlalchemy.orm import relationship

from app.core.database import Base


class Call(Base):

    __tablename__ = "calls"

    call_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    file_name = Column(
        String,
        nullable=False
    )

    call_type = Column(
        String,
        nullable=True,
        default="detecting..."
    )

    audio_path = Column(
        String,
        nullable=False
    )

    duration_seconds = Column(
        Float,
        nullable=True
    )

    processing_status = Column(
        String,
        default="processing"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    transcripts = relationship(
        "Transcript",
        back_populates="call",
        cascade="all, delete"
    )

    summaries = relationship(
        "Summary",
        back_populates="call",
        cascade="all, delete"
    )

    qa_history = relationship(
        "QAHistory",
        back_populates="call",
        cascade="all, delete"
    )

    audio_summaries = relationship(
        "AudioSummary",
        back_populates="call",
        cascade="all, delete"
    )