import enum
from sqlalchemy import text
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Index

from . import Base


class MessageType(enum.Enum):
    AI = "AI"
    HUMAN = "Human"


class MessageHistory(Base):
    __tablename__ = "message_history"

    id = Column(
        Integer, primary_key=True, index=True, autoincrement=True, nullable=False
    )
    user_email = Column(String(50), index=True, nullable=False)
    message = Column(String(5000), nullable=False)
    message_type = Column(String(10), nullable=False)
    created_at = Column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
    )
