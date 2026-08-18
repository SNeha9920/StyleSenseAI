from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String

from app.core.database import Base


class Subscription(Base):
    __tablename__ = "subscriptions"

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

    plan_name = Column(
        String(50),
        nullable=False,
    )

    status = Column(
        String(30),
        default="active",
        nullable=False,
    )

    price = Column(
        Float,
        nullable=True,
    )

    currency = Column(
        String(10),
        default="INR",
        nullable=False,
    )

    start_date = Column(
        DateTime,
        nullable=False,
    )

    end_date = Column(
        DateTime,
        nullable=True,
    )

    auto_renew = Column(
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
