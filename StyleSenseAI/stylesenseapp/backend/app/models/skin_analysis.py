from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    JSON,
)

from app.core.database import Base


class SkinAnalysis(Base):
    __tablename__ = "skin_analysis_history"

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

    # Image used for analysis
    image_url = Column(
        String(500),
        nullable=True,
    )

    # YouCam task information
    youcam_task_id = Column(
        String(255),
        nullable=True,
        unique=True,
        index=True,
    )

    analysis_status = Column(
        String(50),
        nullable=False,
        default="pending",
        index=True,
    )

    # Scores
    skin_health_score = Column(
        Float,
        nullable=True,
    )

    hydration_score = Column(
        Float,
        nullable=True,
    )

    texture_score = Column(
        Float,
        nullable=True,
    )

    brightness_score = Column(
        Float,
        nullable=True,
    )

    acne_score = Column(
        Float,
        nullable=True,
    )

    # AI-generated content
    ai_summary = Column(
        Text,
        nullable=True,
    )

    ai_recommendation = Column(
        Text,
        nullable=True,
    )

    recommended_routine = Column(
        JSON,
        nullable=True,
    )

    recommended_ingredients = Column(
        JSON,
        nullable=True,
    )

    recommended_products = Column(
        JSON,
        nullable=True,
    )

    # Complete YouCam response
    raw_result = Column(
        JSON,
        nullable=True,
    )

    analyzed_at = Column(
        DateTime,
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