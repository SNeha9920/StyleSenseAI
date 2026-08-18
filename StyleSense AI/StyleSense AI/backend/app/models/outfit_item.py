from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, UniqueConstraint

from app.core.database import Base


class OutfitItem(Base):
    __tablename__ = "outfit_items"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    outfit_id = Column(
        Integer,
        ForeignKey("outfits.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    wardrobe_item_id = Column(
        Integer,
        ForeignKey("wardrobe_items.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    display_order = Column(
        Integer,
        default=0,
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

    __table_args__ = (
        UniqueConstraint(
            "outfit_id",
            "wardrobe_item_id",
            name="uq_outfit_wardrobe_item",
        ),
    )