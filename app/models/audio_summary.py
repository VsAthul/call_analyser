from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import String

from sqlalchemy.orm import relationship

from app.core.database import Base


class AudioSummary(Base):

    __tablename__ = "audio_summaries"

    audio_summary_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    call_id = Column(
        Integer,
        ForeignKey("calls.call_id")
    )

    audio_path = Column(
        String,
        nullable=False
    )

    call = relationship(
        "Call",
        back_populates="audio_summaries"
    )