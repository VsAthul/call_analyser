from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import Text, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class Summary(Base):

    __tablename__ = "summaries"

    summary_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    call_id = Column(
        Integer,
        ForeignKey("calls.call_id")
    )

    summary_text = Column(
        Text,
        nullable=False
    )

    audio_summary_path = Column(
        String,
        nullable=True
    )

    call = relationship(
        "Call",
        back_populates="summaries"
    )

    