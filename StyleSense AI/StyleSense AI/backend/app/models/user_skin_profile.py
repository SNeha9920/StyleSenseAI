from datetime import datetime

from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class UserSkinProfile(Base):
    __tablename__ = "user_skin_profile"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    skin_tone_id = Column(
        Integer,
        ForeignKey("skin_tones.id"),
        nullable=True,
    )

    skin_type_id = Column(
        Integer,
        ForeignKey("skin_types.id"),
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

    # Relationships
    user = relationship(
        "User",
        back_populates="skin_profile",
    )

    skin_tone = relationship(
        "SkinTone",
    )

    skin_type = relationship(
        "SkinType",
    )