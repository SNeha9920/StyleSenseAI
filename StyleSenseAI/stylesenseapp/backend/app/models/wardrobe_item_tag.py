from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from app.core.database import Base


class WardrobeItemTag(Base):
    __tablename__ = "wardrobe_item_tags"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    wardrobe_item_id = Column(
        Integer,
        ForeignKey("wardrobe_items.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    tag = Column(
        String(100),
        nullable=False,
        index=True,
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