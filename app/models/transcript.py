from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Text

from sqlalchemy.orm import relationship

from app.core.database import Base


class Transcript(Base):

    __tablename__ = "transcripts"

    transcript_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    call_id = Column(
        Integer,
        ForeignKey("calls.call_id")
    )

    speaker = Column(
        String,
        nullable=False
    )

    text = Column(
        Text,
        nullable=False
    )

    timestamp = Column(
        String,
        nullable=True
    )

    call = relationship(
        "Call",
        back_populates="transcripts"
    )