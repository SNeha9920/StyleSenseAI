from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text

from app.core.database import Base


class Outfit(Base):
    __tablename__ = "outfits"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )

    name = Column(
        String(200),
        nullable=False,
    )

    description = Column(
        Text,
        nullable=True,
    )

    occasion_id = Column(
        Integer,
        ForeignKey("occasions.id"),
        nullable=True,
    )

    season_id = Column(
        Integer,
        ForeignKey("seasons.id"),
        nullable=True,
    )

    style_id = Column(
        Integer,
        ForeignKey("styles.id"),
        nullable=True,
    )

    image_url = Column(
        String(500),
        nullable=True,
    )

    match_score = Column(
        Float,
        nullable=True,
    )

    is_ai_generated = Column(
        Boolean,
        default=True,
        nullable=False,
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