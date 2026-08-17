from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text

from app.core.database import Base


class VirtualTryOn(Base):
    __tablename__ = "virtual_tryons"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    original_image_url = Column(
        String(500),
        nullable=True,
    )

    result_image_url = Column(
        String(500),
        nullable=True,
    )

    outfit_id = Column(
        Integer,
        ForeignKey("outfits.id"),
        nullable=True,
    )

    match_score = Column(
        Float,
        nullable=True,
    )

    ai_description = Column(
        Text,
        nullable=True,
    )

    status = Column(
        String(50),
        default="pending",
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