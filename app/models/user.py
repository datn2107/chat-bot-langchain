import enum
from sqlalchemy import text
from sqlalchemy import Column, String, Integer, DateTime

from . import Base

class AccountType(enum.Enum):
    FREE = "Free"
    STANDARD = "Standard"
    PREMIUM = "Premium"

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    account_type = Column(String(10), default=AccountType.FREE.value, nullable=False)
    expire_date = Column(DateTime, default='9999-01-01 00:00:00', nullable=False)
    created_at = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'), nullable=False)
    updated_at = Column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=False)
