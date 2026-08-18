from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Float

from app.core.database import Base


class UserSetting(Base):
    __tablename__ = "user_settings"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )

    theme = Column(
        String(20),
        default="light",
        nullable=False,
    )

    accent_color = Column(
        String(30),
        default="violet",
        nullable=False,
    )

    ai_personality = Column(
        String(50),
        default="Fashion Expert",
        nullable=True,
    )

    response_length = Column(
        String(30),
        default="Short",
        nullable=True,
    )

    creativity = Column(
        Float,
        default=0.7,
        nullable=True,
    )

    ai_analysis_complete = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    weekly_fashion_report = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    product_recommendations = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    wardrobe_suggestions = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    new_features_updates = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    save_uploaded_photos = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    ai_personalization = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    anonymous_analytics = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    face_detection_permission = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    location_access = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    two_factor_authentication = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    login_alerts = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    show_active_sessions = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    trusted_devices = Column(
        Boolean,
        default=False,
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