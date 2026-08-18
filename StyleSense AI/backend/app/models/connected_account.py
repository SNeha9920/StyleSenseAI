from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String

from app.core.database import Base


class ConnectedAccount(Base):
    __tablename__ = "connected_accounts"

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

    provider = Column(
        String(50),
        nullable=False,
        index=True,
    )

    provider_account_id = Column(
        String(255),
        nullable=True,
    )

    access_token = Column(
        String(1000),
        nullable=True,
    )

    refresh_token = Column(
        String(1000),
        nullable=True,
    )

    is_connected = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    connected_at = Column(
        DateTime,
        default=datetime.utcnow,
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