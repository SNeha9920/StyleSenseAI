from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text

from app.core.database import Base


class WardrobeItem(Base):
    __tablename__ = "wardrobe_items"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    name = Column(
        String(200),
        nullable=False,
    )

    image_url = Column(
        String(500),
        nullable=True,
    )

    brand_id = Column(
        Integer,
        ForeignKey("brands.id"),
        nullable=True,
    )

    category_id = Column(
        Integer,
        ForeignKey("clothing_categories.id"),
        nullable=True,
    )

    color_id = Column(
        Integer,
        ForeignKey("colors.id"),
        nullable=True,
    )

    season_id = Column(
        Integer,
        ForeignKey("seasons.id"),
        nullable=True,
    )

    occasion_id = Column(
        Integer,
        ForeignKey("occasions.id"),
        nullable=True,
    )

    style_id = Column(
        Integer,
        ForeignKey("styles.id"),
        nullable=True,
    )

    size = Column(
        String(30),
        nullable=True,
    )

    material = Column(
        String(100),
        nullable=True,
    )

    purchase_price = Column(
        Float,
        nullable=True,
    )

    purchase_date = Column(
        DateTime,
        nullable=True,
    )

    notes = Column(
        Text,
        nullable=True,
    )

    is_favorite = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    is_active = Column(
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