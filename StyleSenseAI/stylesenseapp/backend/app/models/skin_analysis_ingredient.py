from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text, UniqueConstraint

from app.core.database import Base


class SkinAnalysisIngredient(Base):
    __tablename__ = "skin_analysis_ingredients"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    skin_analysis_id = Column(
        Integer,
        ForeignKey("skin_analysis_history.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    ingredient_id = Column(
        Integer,
        ForeignKey("ingredients.id"),
        nullable=False,
        index=True,
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
            "ingredient_id",
            name="uq_skin_analysis_ingredient",
        ),
    )