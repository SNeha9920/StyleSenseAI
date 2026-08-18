from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    Text,
    UniqueConstraint,
)

from app.core.database import Base


class SkinAnalysisConcern(Base):
    __tablename__ = "skin_analysis_concerns"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    skin_analysis_id = Column(
        Integer,
        ForeignKey(
            "skin_analysis_history.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    skin_concern_id = Column(
        Integer,
        ForeignKey(
            "skin_concerns.id",
        ),
        nullable=False,
        index=True,
    )

    score = Column(
        Float,
        nullable=True,
    )

    recommendation_reason = Column(
        Text,
        nullable=True,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint(
            "skin_analysis_id",
            "skin_concern_id",
            name="uq_skin_analysis_concern",
        ),
    )