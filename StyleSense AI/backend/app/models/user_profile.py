from datetime import datetime

from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class UserProfile(Base):
    __tablename__ = "user_profiles"

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

    phone = Column(
        String(20),
        nullable=True,
    )

    location = Column(
        String(255),
        nullable=True,
    )

    date_of_birth = Column(
        Date,
        nullable=True,
    )

    # Body Profile
    height_cm = Column(
        Float,
        nullable=True,
    )

    weight_kg = Column(
        Float,
        nullable=True,
    )

    body_type_id = Column(
        Integer,
        ForeignKey("body_types.id"),
        nullable=True,
        index=True,
    )

    fit_preference_id = Column(
        Integer,
        ForeignKey("fit_preferences.id"),
        nullable=True,
        index=True,
    )

    # Shopping Preferences
    budget = Column(
        Float,
        nullable=True,
    )

    shopping_frequency = Column(
        String(50),
        nullable=True,
    )

    preferred_shopping = Column(
        String(100),
        nullable=True,
    )

    sustainable_fashion = Column(
        String(20),
        nullable=True,
    )

    # Measurements
    chest_cm = Column(
        Float,
        nullable=True,
    )

    waist_cm = Column(
        Float,
        nullable=True,
    )

    hip_cm = Column(
        Float,
        nullable=True,
    )

    shoulder_cm = Column(
        Float,
        nullable=True,
    )

    sleeve_length_cm = Column(
        Float,
        nullable=True,
    )

    shoe_size = Column(
        Float,
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
        back_populates="profile",
    )

    body_type = relationship(
        "BodyType",
    )

    fit_preference = relationship(
        "FitPreference",
    )