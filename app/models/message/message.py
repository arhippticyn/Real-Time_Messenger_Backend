from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Enum, DateTime, ForeignKey
from sqlalchemy.sql import func
from ...db.base import Base
import enum

class MessageType(str, enum.Enum):
    text = 'text'
    image = 'image'

class Message(Base):
    __tablename__ = 'message'

    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey('chats.id'))
    sender_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    content: Mapped[str | None] = mapped_column(nullable=True)
    type: Mapped[MessageType] = mapped_column(Enum(MessageType))
    file_url: Mapped[str | None] = mapped_column()
    created_at: Mapped[DateTime] = mapped_column(default=func.now())

    sender: Mapped['User'] = relationship('User', foreign_keys=[sender_id])
    chat: Mapped['Chat'] = relationship('Chat', foreign_keys=[chat_id])
