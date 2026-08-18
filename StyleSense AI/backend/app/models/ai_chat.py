from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text

from app.core.database import Base


class AIChatSession(Base):
    __tablename__ = "ai_chat_sessions"

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

    title = Column(
        String(255),
        nullable=True,
    )

    context_type = Column(
        String(50),
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


class AIChatMessage(Base):
    __tablename__ = "ai_chat_messages"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    session_id = Column(
        Integer,
        ForeignKey("ai_chat_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    role = Column(
        String(20),
        nullable=False,
    )

    message = Column(
        Text,
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