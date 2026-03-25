from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Enum, DateTime
from ...db.base import Base
import enum
from sqlalchemy.sql import func
from datetime import datetime

class MessageStatusType(str, enum.Enum):
    sent = 'sent'
    delivered = 'delivered'
    read = 'read'


class MessageStatus(Base):
    __tablename__ = 'message_status'

    id: Mapped[int] = mapped_column(primary_key=True)
    message_id: Mapped[int] = mapped_column(ForeignKey('message.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    status: Mapped[MessageStatusType] = mapped_column(Enum(MessageStatusType))
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    message: Mapped['Message'] = relationship('Message', foreign_keys=[message_id])
    user: Mapped['User'] = relationship('User', foreign_keys=[user_id])