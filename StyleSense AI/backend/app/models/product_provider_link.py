from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, UniqueConstraint

from app.core.database import Base


class ProductProviderLink(Base):
    __tablename__ = "product_provider_links"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    skincare_product_id = Column(
        Integer,
        ForeignKey("skincare_products.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    provider_id = Column(
        Integer,
        ForeignKey("shopping_providers.id"),
        nullable=False,
        index=True,
    )

    product_url = Column(
        String(1000),
        nullable=False,
    )

    provider_product_id = Column(
        String(255),
        nullable=True,
    )

    price = Column(
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

    __table_args__ = (
        UniqueConstraint(
            "skincare_product_id",
            "provider_id",
            name="uq_product_provider",
        ),
    )